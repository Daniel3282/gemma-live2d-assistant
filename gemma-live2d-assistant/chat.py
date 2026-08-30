import os
import wave
import numpy as np
import sounddevice as sd
import pyautogui
from huggingface_hub import hf_hub_download
import litert_lm
from PySide6.QtCore import QThread, Signal

try:
    from supertonic import TTS
except ImportError:
    TTS = None

class VoiceAssistantWorker(QThread):
    status_changed = Signal(str)       # "idle", "listening", "processing", "speaking"
    speech_amplitude = Signal(float)  # Moves the mouth parameter of the Live2D model
    text_received = Signal(str)       # AI-generated response text
    vision_text_received = Signal(str) # Text generated during screen analysis

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True
        self.engine = None
        self.conversation = None
        self.tts_engine = None
        self.voice_style = None
        
        # Flag to reset the conversation if the language is changed
        self.reset_conversation_flag = False
        
        # Default prompts (fallback if prompts.json fails to load)
        self.prompt_instruction = (
            "IMPORTANT: ACCURATELY INTERPRET THE USER'S MESSAGE AND NEVER, UNDER ANY CIRCUMSTANCE, "
            "SEND THE TAG [PRINT] IF THE USER'S REQUEST DOES NOT CLEARLY FIT A CONTEXT WHERE THEY ASKED TO SEE THEIR SCREEN! "
            "Respond as a human in a friendly and natural way in English. "
            "IF the user asks you to see their screen, look at the monitor, or check what is open, "
            "your response MUST start with the tag [PRINT] followed by a creative and natural phrase "
            "letting them know you are going to check (e.g.: '[PRINT] Sure, let me take a quick look at your screen!'). "
            "If they did not ask to see the screen, respond normally without the tag. "
            "ALWAYS SEND A CLEAN MESSAGE WITHOUT ANY EXTRA MARKUP OR SYMBOLS."
        )
        
        self.prompt_vision = (
            "Analyze this image of my screen and describe a summary of what it is about, in a direct way and without introductory phrases."
        )
        
        self.voice_name = "F1"
        self.voice_lang = "en"  # Default initial language set to English
        
        self.repo_id = "litert-community/gemma-4-E2B-it-litert-lm"
        self.filename = "gemma-4-E2B-it.litertlm"
        self.voice_speed = 1.4
        self.voice_steps = 8
        self.sample_rate = 16000  
        self.speech_threshold = 0.015  
        self.silence_limit = 1.5
        self.pre_buffer_size = 6
        
        # --- Noise Reduction Settings ---
        self.required_speech_blocks = 3  
        
        self.temp_audio = "temp_input_voice.wav"
        self.temp_screenshot = "temp_screen_print.png"
        self.interaction_count = 0
        
        # Silero VAD state
        self.use_silero = False
        self.vad_model = None

    def run(self):
        self.status_changed.emit("initializing")
        
        # 1. Silero VAD setup
        try:
            import torch
            from silero_vad import load_silero_vad
            
            torch.set_num_threads(1)
            self.vad_model = load_silero_vad(onnx=True)
            self.use_silero = True
            print("🎙️ [Silero VAD]: Voice detection engine activated!")
        except Exception as e:
            print(f"⚠️ Could not start Silero VAD ({e}). Using amplitude detection instead.")
            self.use_silero = False

        # 2. Gemma Model initialization
        try:
            model_path = hf_hub_download(
                repo_id=self.repo_id,
                filename=self.filename,
                local_dir="./models" 
            )
            self.engine = litert_lm.Engine(
                model_path,
                backend=litert_lm.Backend.GPU(),
                audio_backend=litert_lm.Backend.CPU(),
                vision_backend=litert_lm.Backend.CPU()
            )
            self.conversation = self.engine.create_conversation()

        except Exception as e:
            self.text_received.emit(f"Error loading Gemma model: {e}")
            return

        # 3. Supertonic 3 initialization
        if TTS is not None:
            try:
                self.tts_engine = TTS(auto_download=True)
                self.voice_style = self.tts_engine.get_voice_style(voice_name=self.voice_name)
            except Exception as e:
                self.text_received.emit(f"⚠️ Error starting Supertonic: {e}. No audio output will be active.")
        else:
            self.text_received.emit("⚠️ Supertonic library not found.")

        self.status_changed.emit("idle")

        # Main Loop
        while self.running:
            # Check if a request was made to reset the conversation to switch languages
            if self.reset_conversation_flag:
                if self.engine:
                    try:
                        self.conversation = self.engine.create_conversation()
                        self.interaction_count = 0
                        print("🧹 [Language Switch]: Conversation successfully reset due to language change!")
                    except Exception as err:
                        print(f"⚠️ Error resetting conversation: {err}")
                self.reset_conversation_flag = False

            recording_data = []
            pre_buffer = []
            grid_state = "idle"
            silence_timer = 0.0
            block_duration = 1024 / self.sample_rate
            
            consecutive_speech_blocks = 0

            if self.use_silero and self.vad_model:
                try:
                    self.vad_model.reset_states()
                except Exception:
                    pass

            def callback(indata, frames, time_info, status):
                nonlocal grid_state, silence_timer, recording_data, pre_buffer, consecutive_speech_blocks
                
                is_speech = False
                if self.use_silero:
                    try:
                        import torch
                        audio_chunk = torch.from_numpy(indata.squeeze().astype(np.float32))
                        speech_prob = self.vad_model(audio_chunk, 16000).item()
                        is_speech = speech_prob > 0.85
                    except Exception:
                        volume = float(np.abs(indata).mean())
                        is_speech = volume > self.speech_threshold
                else:
                    volume = float(np.abs(indata).mean())
                    is_speech = volume > self.speech_threshold

                if grid_state == "idle":
                    pre_buffer.append(indata.copy())
                    if len(pre_buffer) > self.pre_buffer_size:
                        pre_buffer.pop(0)

                    if is_speech:
                        consecutive_speech_blocks += 1
                        if consecutive_speech_blocks >= self.required_speech_blocks:
                            grid_state = "recording"
                            self.status_changed.emit("listening")
                            recording_data = list(pre_buffer)
                            pre_buffer.clear()
                            silence_timer = 0.0
                    else:
                        consecutive_speech_blocks = 0
                
                elif grid_state == "recording":
                    recording_data.append(indata.copy())
                    if not is_speech:
                        grid_state = "silence_counting"
                        silence_timer = 0.0
                elif grid_state == "silence_counting":
                    recording_data.append(indata.copy())
                    if is_speech:
                        grid_state = "recording"
                        silence_timer = 0.0
                    else:
                        silence_timer += block_duration

            try:
                with sd.InputStream(samplerate=self.sample_rate, channels=1, callback=callback, dtype='float32', blocksize=1024):
                    while (grid_state != "silence_counting" or silence_timer < self.silence_limit) and self.running:
                        sd.sleep(50)
            except Exception as e:
                sd.sleep(1000)
                continue

            if not self.running:
                break

            if not recording_data:
                continue

            self.status_changed.emit("processing")
            audio_array = np.concatenate(recording_data, axis=0)
            audio_array = np.clip(audio_array, -1.0, 1.0)
            int_data = (audio_array * 32767).astype(np.int16)

            with wave.open(self.temp_audio, "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(int_data.tobytes())

            try:
                self.interaction_count += 1
                if self.interaction_count > 6:
                    self.text_received.emit("🧹 [Maintenance]: Clearing chat history...")
                    self.conversation = self.engine.create_conversation()
                    self.interaction_count = 0

                contents = [
                    self.prompt_instruction,
                    litert_lm.Content.AudioFile(absolute_path=self.temp_audio)
                ]

                response = self.conversation.send_message(litert_lm.Contents.of(*contents))
                resposta_texto = response["content"][0]["text"]
                self.text_received.emit(resposta_texto)

                if "[PRINT]" in resposta_texto:
                    import threading
                    vision_result = []
                    
                    def async_vision_analysis():
                        try:
                            screenshot = pyautogui.screenshot()
                            screenshot.save(self.temp_screenshot)

                            contents_visao = [
                                self.prompt_vision,
                                litert_lm.Content.ImageFile(absolute_path=self.temp_screenshot)
                            ]
                            response_visao = self.conversation.send_message(litert_lm.Contents.of(*contents_visao))
                            resposta_visao_texto = response_visao["content"][0]["text"]
                            vision_result.append(resposta_visao_texto)
                        except Exception as err:
                            print(f"Error in parallel vision analysis: {err}")
                        finally:
                            if os.path.exists(self.temp_screenshot):
                                try:
                                    os.remove(self.temp_screenshot)
                                except:
                                    pass

                    vt = threading.Thread(target=async_vision_analysis, daemon=True)
                    vt.start()

                    self.speak_text(resposta_texto)

                    if vt.is_alive():
                        self.status_changed.emit("processing")

                    vt.join()

                    if vision_result:
                        resposta_visao_texto = vision_result[0]
                        self.vision_text_received.emit(resposta_visao_texto)
                        self.speak_text(resposta_visao_texto)
                else:
                    self.speak_text(resposta_texto)

            except Exception as e:
                self.text_received.emit(f"AI Processing error: {e}")
            finally:
                if os.path.exists(self.temp_audio):
                    try:
                        os.remove(self.temp_audio)
                    except:
                        pass
            
            self.status_changed.emit("idle")

    def speak_text(self, text):
        if not self.tts_engine:
            return
        
        clean_text = text.replace("[PRINT]", "").strip()
        if not clean_text:
            return

        try:
            self.voice_style = self.tts_engine.get_voice_style(voice_name=self.voice_name)
        except Exception as e:
            print(f"⚠️ Error updating voice style '{self.voice_name}': {e}")
            if not self.voice_style:
                return

        import re
        import queue
        import threading

        sentences = re.split(r'(?<=[.!?])\s+', clean_text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return

        audio_queue = queue.Queue(maxsize=3)
        self.status_changed.emit("speaking")

        def producer():
            for s in sentences:
                if not self.running:
                    break
                try:
                    audio_data, duration = self.tts_engine.synthesize(
                        text=s,
                        voice_style=self.voice_style,
                        speed=self.voice_speed,
                        total_steps=self.voice_steps,
                        lang=self.voice_lang
                    )
                    
                    sr = 44100
                    if hasattr(audio_data, "numpy"):
                        audio_data = audio_data.numpy()
                    audio_data = np.array(audio_data).squeeze()
                    
                    audio_queue.put((audio_data, sr))
                except Exception as e:
                    print(f"Error in parallel segment synthesis: {e}")
            
            audio_queue.put(None)

        thread_sintese = threading.Thread(target=producer, daemon=True)
        thread_sintese.start()

        chunk_size = 1024
        try:
            with sd.OutputStream(samplerate=44100, channels=1, dtype='float32') as stream:
                while self.running:
                    item = audio_queue.get()
                    if item is None:
                        break
                    
                    audio_data, sr = item
                    
                    for i in range(0, len(audio_data), chunk_size):
                        if not self.running:
                            break
                        chunk = audio_data[i:i+chunk_size]
                        if len(chunk) < chunk_size:
                            chunk = np.pad(chunk, (0, chunk_size - len(chunk)))
                        stream.write(chunk)
                        
                        rms = np.sqrt(np.mean(chunk**2))
                        amplitude = min(1.0, float(rms * 6.0))
                        self.speech_amplitude.emit(amplitude)
                        
        except Exception as e:
            print(f"Error in continuous audio playback: {e}")

        self.speech_amplitude.emit(0.0)

    def stop(self):
        self.running = False
        self.wait()