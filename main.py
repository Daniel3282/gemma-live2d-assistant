import sys
import os
import ctypes
import random  
import json  # Imported to parse and read the prompts.json configuration
from PySide6.QtCore import Qt, QTimer, QSettings, QPoint, Signal, QEvent, QLocale
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenu, QDialog, QVBoxLayout, 
    QHBoxLayout, QTabWidget, QWidget, QLabel, QTextEdit, 
    QComboBox, QPushButton
)
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from pynput import mouse, keyboard
import live2d.v2 as live2d

from chat import VoiceAssistantWorker


def load_prompts_from_json(lang_code):
    """Utility function to read prompts locally from prompts.json with fallback to English"""
    try:
        filepath = os.path.join(os.path.dirname(__file__), "prompts.json") if "__file__" in globals() else "prompts.json"
        if not os.path.exists(filepath):
            filepath = "prompts.json"
            
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        lang_data = data.get(lang_code, data.get("en", {}))
        return lang_data.get("instruction", ""), lang_data.get("vision", "")
    except Exception as e:
        print(f"⚠️ Error reading prompts.json: {e}")
        return "", ""


class SettingsDialog(QDialog):
    """Configuration Dialog Organized in Tabs"""
    def __init__(self, current_prompt, current_vision, current_voice, current_lang, parent=None):
        super().__init__(parent)
        self.main_window = parent  # Reference to the MainWindow
        self.current_vision_prompt = current_vision
        self.setWindowTitle("Assistant Settings")
        self.resize(520, 450)
        
        layout = QVBoxLayout(self)
        self.tabs = QTabWidget(self)
        
        # --- TAB 1: System Prompt ---
        self.tab_prompt = QWidget()
        prompt_layout = QVBoxLayout(self.tab_prompt)
        prompt_layout.addWidget(QLabel("Default Instruction Prompt (Gemma 4):"))
        
        self.prompt_edit = QTextEdit()
        self.prompt_edit.setPlainText(current_prompt)
        prompt_layout.addWidget(self.prompt_edit)
        self.tabs.addTab(self.tab_prompt, "System Prompt")
        
        # --- TAB 2: Voice & Language ---
        self.tab_voice = QWidget()
        voice_layout = QVBoxLayout(self.tab_voice)
        
        # Voice Style
        voice_layout.addWidget(QLabel("Voice Style Code (Supertonic 3):"))
        self.voice_combo = QComboBox()
        self.voice_combo.addItems(["F1", "F2", "F3", "F4", "F5", "M1", "M2", "M3", "M4", "M5"])
        self.voice_combo.setCurrentText(current_voice)
        voice_layout.addWidget(self.voice_combo)
        
        voice_layout.addSpacing(10)
        
        # Language
        voice_layout.addWidget(QLabel("Voice Language:"))
        self.lang_combo = QComboBox()
        
        self.languages_list = [
            ("Arabic (ar)", "ar"), ("Bulgarian (bg)", "bg"), ("Croatian (hr)", "hr"),
            ("Czech (cs)", "cs"), ("Danish (da)", "da"), ("Dutch (nl)", "nl"),
            ("English (en)", "en"), ("Estonian (et)", "et"), ("Finnish (fi)", "fi"),
            ("French (fr)", "fr"), ("German (de)", "de"), ("Greek (el)", "el"),
            ("Hindi (hi)", "hi"), ("Hungarian (hu)", "hu"), ("Indonesian (id)", "id"),
            ("Italian (it)", "it"), ("Japanese (ja)", "ja"), ("Korean (ko)", "ko"),
            ("Latvian (lv)", "lv"), ("Lithuanian (lt)", "lt"), ("Polish (pl)", "pl"),
            ("Portuguese (pt)", "pt"), ("Romanian (ro)", "ro"), ("Russian (ru)", "ru"),
            ("Slovak (sk)", "sk"), ("Slovenian (sl)", "sl"), ("Spanish (es)", "es"),
            ("Swedish (sv)", "sv"), ("Turkish (tr)", "tr"), ("Ukrainian (uk)", "uk"),
            ("Vietnamese (vi)", "vi")
        ]
        
        for name, code in self.languages_list:
            self.lang_combo.addItem(name, code)
            
        index_lang = self.lang_combo.findData(current_lang)
        if index_lang != -1:
            self.lang_combo.setCurrentIndex(index_lang)
            
        voice_layout.addWidget(self.lang_combo)
        
        voice_layout.addSpacing(15)
        
        # Button to instantly load language preset configuration
        self.btn_adapt = QPushButton("Apply Language Preset (Load from JSON)")
        self.btn_adapt.clicked.connect(self.apply_language_preset)
        voice_layout.addWidget(self.btn_adapt)
        
        voice_layout.addStretch()
        
        self.tabs.addTab(self.tab_voice, "Voice & Language")
        
        layout.addWidget(self.tabs)
        
        # --- Action Buttons ---
        buttons_layout = QHBoxLayout()
        self.btn_save = QPushButton("Save")
        self.btn_cancel = QPushButton("Cancel")
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_save)
        buttons_layout.addWidget(self.btn_cancel)
        layout.addLayout(buttons_layout)
        
        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def apply_language_preset(self):
        """Loads and defines matching prompts instantly from the JSON configuration"""
        target_lang = self.lang_combo.currentData()
        inst, vis = load_prompts_from_json(target_lang)
        if inst:
            self.prompt_edit.setPlainText(inst)
            self.current_vision_prompt = vis
            print(f"⚙️ Language preset '{target_lang}' successfully loaded.")
        else:
            print(f"⚠️ Could not find or load presets for '{target_lang}'.")

    def accept(self):
        super().accept()

    def reject(self):
        super().reject()

    def get_settings(self):
        return (
            self.prompt_edit.toPlainText(),
            self.current_vision_prompt,
            self.voice_combo.currentText(),
            self.lang_combo.currentData()
        )


class Live2DWidget(QOpenGLWidget):
    def __init__(self, model_path, parent=None):
        super().__init__(parent)
        self.model_path = model_path
        self.model = None
        
        self.mouse_x = 0.0
        self.mouse_y = 0.0
        self.target_mouse_x = 0.0
        self.target_mouse_y = 0.0
        
        self.attention_mode = False
        self.mouth_open = 0.0  

    def initializeGL(self):
        try:
            live2d.init()
        except Exception as e:
            print(f"Initialization error: {e}")
            return

        try:
            self.model = live2d.LAppModel()
            self.model.LoadModelJson(self.model_path.replace("\\", "/"))
            self.model.Resize(self.width(), self.height())
        except Exception as e:
            print(f"Error loading model: {e}")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)

    def resizeGL(self, w, h):
        if self.model:
            self.model.Resize(w, h)

    def paintGL(self):
        live2d.clearBuffer(0.0, 0.0, 0.0, 0.0)

        if self.model:
            try:
                self.model.Update()

                if hasattr(self.model, "SetParameterValue"):
                    if self.attention_mode:
                        target_x = 0.0
                        target_y = 0.0
                    else:
                        target_x = self.target_mouse_x
                        target_y = self.target_mouse_y

                    self.mouse_x += (target_x - self.mouse_x) * 0.08
                    self.mouse_y += (target_y - self.mouse_y) * 0.08

                    self.model.SetParameterValue("PARAM_ANGLE_X", self.mouse_x * 30.0, 1.0)
                    self.model.SetParameterValue("PARAM_ANGLE_Y", self.mouse_y * 30.0, 1.0)
                    self.model.SetParameterValue("PARAM_EYE_BALL_X", self.mouse_x, 1.0)
                    self.model.SetParameterValue("PARAM_EYE_BALL_Y", self.mouse_y, 1.0)
                    
                    self.model.SetParameterValue("PARAM_MOUTH_OPEN_Y", self.mouth_open, 1.0)

                self.model.Draw()
            except Exception as e:
                print(f"Render error: {e}")

    def closeEvent(self, event):
        try:
            live2d.dispose()
        except Exception:
            pass
        super().closeEvent(event)


class MainWindow(QMainWindow):
    click_through_signal = Signal(bool)

    def __init__(self, model_path):
        super().__init__()
        self.setWindowTitle("Live2D Assistant Avatar")
        
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setMouseTracking(True)

        self.settings = QSettings("Live2DViewer", "AppConfig")
        if self.settings.contains("geometry"):
            self.restoreGeometry(self.settings.value("geometry"))
        else:
            self.resize(400, 600)

        self.gl_widget = Live2DWidget(model_path, self)
        self.gl_widget.setMouseTracking(True)
        self.gl_widget.installEventFilter(self)
        self.setCentralWidget(self.gl_widget)

        self.click_through_signal.connect(self.apply_click_through)

        self.ctrl_pressed = False
        self.drag_position = QPoint()
        self.resize_edge = None
        self.margin = 10

        self.apply_click_through(True)
        self.init_listeners()

        if sys.platform == "win32":
            try:
                hwnd = int(self.winId())
                ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, 0x00000011)
                print("🖥️ [System]: Invisible screenshot mode natively activated.")
            except Exception as e:
                print(f"Could not apply native window concealment: {e}")

        # --- Automatic System Language Detection (Fallback) ---
        supported_langs = [
            "ar", "bg", "hr", "cs", "da", "nl", "en", "et", "fi", "fr", "de", "el", "hi", 
            "hu", "id", "it", "ja", "ko", "lv", "lt", "pl", "pt", "ro", "ru", "sk", "sl", 
            "es", "sv", "tr", "uk", "vi"
        ]
        
        sys_locale = QLocale.system().name().split('_')[0].lower()
        if sys_locale not in supported_langs:
            detected_lang = "en"
        else:
            detected_lang = sys_locale

        if not self.settings.contains("voice_lang"):
            self.settings.setValue("voice_lang", detected_lang)
            print(f"🌐 [Language]: System language detected and activated: {detected_lang}")

        saved_lang = self.settings.value("voice_lang")
        saved_voice = self.settings.value("voice_name", "F1")

        # If saved prompts do not exist in local configurations, load from JSON file
        if not self.settings.contains("prompt_instrucao") or not self.settings.value("prompt_instrucao"):
            inst, vis = load_prompts_from_json(saved_lang)
            self.settings.setValue("prompt_instrucao", inst)
            self.settings.setValue("prompt_visao", vis)
            print(f"💾 [Settings]: Preset prompts applied for language '{saved_lang}'")

        saved_prompt = self.settings.value("prompt_instrucao")
        saved_vision_prompt = self.settings.value("prompt_visao")

        # --- Voice Assistant Integration ---
        self.assistant = VoiceAssistantWorker()
        self.assistant.voice_lang = saved_lang
        self.assistant.voice_name = saved_voice
        self.assistant.prompt_instruction = saved_prompt
        self.assistant.prompt_vision = saved_vision_prompt
        
        self.assistant.status_changed.connect(self.on_assistant_status_changed)
        self.assistant.speech_amplitude.connect(self.on_speech_amplitude_received)
        self.assistant.text_received.connect(self.on_text_received)
        self.assistant.vision_text_received.connect(self.on_vision_text_received)
        
        self.assistant.voice_speed = 1.35
        self.assistant.silence_limit = 1.6
        self.assistant.speech_threshold = 0.009
        
        self.assistant.start()

    def apply_click_through(self, transparent):
        self.setAttribute(Qt.WA_TransparentForMouseEvents, transparent)
        if sys.platform == "win32":
            hwnd = int(self.winId())
            ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
            if transparent:
                ctypes.windll.user32.SetWindowLongW(hwnd, -20, ex_style | 0x00080000 | 0x00000020)
            else:
                ctypes.windll.user32.SetWindowLongW(hwnd, -20, ex_style & ~0x00000020)

    def init_listeners(self):
        def on_move(x, y):
            screen = QApplication.primaryScreen().geometry()
            window_center_x = self.x() + (self.width() / 2)
            window_center_y = self.y() + (self.height() / 2)

            diff_x = x - window_center_x
            diff_y = y - window_center_y

            self.gl_widget.target_mouse_x = max(-1.0, min(1.0, diff_x / (screen.width() / 2)))
            self.gl_widget.target_mouse_y = max(-1.0, min(1.0, -diff_y / (screen.height() / 2)))

        self.mouse_listener = mouse.Listener(on_move=on_move)
        self.mouse_listener.daemon = True
        self.mouse_listener.start()

        def on_press(key):
            if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
                if not self.ctrl_pressed:
                    self.ctrl_pressed = True
                    self.click_through_signal.emit(False)

        def on_release(key):
            if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
                self.ctrl_pressed = False
                self.click_through_signal.emit(True)
                self.setCursor(Qt.ArrowCursor)
                self.resize_edge = None

        self.keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.keyboard_listener.daemon = True
        self.keyboard_listener.start()

    def on_assistant_status_changed(self, status):
        print(f"[Assistant - Status]: {status.upper()}")
        
        if status in ("listening", "speaking"):
            self.gl_widget.attention_mode = True
        else:
            self.gl_widget.attention_mode = False

        if status == "speaking":
            self.play_random_motion()

    def play_random_motion(self):
        if not self.gl_widget.model:
            return
            
        motions_pool = [
            "shake", "flick_head", "tap_face", "tap_breast", 
            "tap_leg", "tap_belly", "mail", "activity", 
            "born", "friend", "morning", "afternoon", "evening"
        ]
        
        chosen_group = random.choice(motions_pool)
        
        try:
            priority_val = 3
            if hasattr(live2d, "MotionPriority"):
                priority_val = live2d.MotionPriority.FORCE
                
            self.gl_widget.model.StartMotion(chosen_group, 0, priority_val)
            print(f"🎬 [Live2D]: Selected and started motion -> {chosen_group}")
        except Exception as e:
            print(f"Error starting motion {chosen_group}: {e}")

    def on_speech_amplitude_received(self, amplitude):
        self.gl_widget.mouth_open = amplitude

    def on_text_received(self, text):
        print(f"🤖 Gemma: {text}")

    def on_vision_text_received(self, text):
        print(f"🖥️ Gemma (Vision): {text}")

    def get_resize_edge(self, pos):
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()
        m = self.margin

        left = x < m
        right = x > w - m
        top = y < m
        bottom = y > h - m

        if top and left: return "top_left"
        if top and right: return "top_right"
        if bottom and left: return "bottom_left"
        if bottom and right: return "bottom_right"
        if left: return "left"
        if right: return "right"
        if top: return "top"
        if bottom: return "bottom"
        return None

    def eventFilter(self, obj, event):
        if obj == self.gl_widget:
            if event.type() == QEvent.Type.MouseMove:
                self.handle_mouse_move(event)
            elif event.type() == QEvent.Type.MouseButtonPress:
                self.handle_mouse_press(event)
        return super().eventFilter(obj, event)

    def handle_mouse_press(self, event):
        if self.ctrl_pressed:
            if event.button() == Qt.LeftButton:
                self.resize_edge = self.get_resize_edge(event.position().toPoint())
                if not self.resize_edge:
                    self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            elif event.button() == Qt.RightButton:
                self.show_context_menu(event.globalPosition().toPoint())

    def show_context_menu(self, global_pos):
        menu = QMenu(self)
        config_action = menu.addAction("Settings")
        
        selected_action = menu.exec(global_pos)
        if selected_action == config_action:
            self.open_settings_dialog()

    def open_settings_dialog(self):
        dialog = SettingsDialog(
            current_prompt=self.assistant.prompt_instruction,
            current_vision=self.assistant.prompt_vision,
            current_voice=self.assistant.voice_name,
            current_lang=self.assistant.voice_lang,
            parent=self
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_prompt, new_vision, new_voice, new_lang = dialog.get_settings()
            
            # Detects if a change in language code actually occurred
            old_lang = self.assistant.voice_lang
            lang_changed = (old_lang != new_lang)
            
            self.settings.setValue("prompt_instrucao", new_prompt)
            self.settings.setValue("prompt_visao", new_vision)
            self.settings.setValue("voice_name", new_voice)
            self.settings.setValue("voice_lang", new_lang)
            
            self.assistant.prompt_instruction = new_prompt
            self.assistant.prompt_vision = new_vision
            self.assistant.voice_name = new_voice
            self.assistant.voice_lang = new_lang
            
            # Alerts the worker thread to clean up and reset conversation states instantly
            if lang_changed:
                self.assistant.reset_conversation_flag = True
                self.assistant.text_received.emit("🧹 [Language Switch]: New language detected. Starting a new conversation...")
            
            print("⚙️ [Settings]: Settings updated and saved!")

    def handle_mouse_move(self, event):
        if self.ctrl_pressed:
            if not event.buttons() & Qt.LeftButton:
                edge = self.get_resize_edge(event.position().toPoint())
                if edge in ("top_left", "bottom_right"): self.setCursor(Qt.SizeFDiagCursor)
                elif edge in ("top_right", "bottom_left"): self.setCursor(Qt.SizeBDiagCursor)
                elif edge in ("left", "right"): self.setCursor(Qt.SizeHorCursor)
                elif edge in ("top", "bottom"): self.setCursor(Qt.SizeVerCursor)
                else: self.setCursor(Qt.ArrowCursor)
            else:
                rect = self.geometry()
                global_pos = event.globalPosition().toPoint()

                if self.resize_edge:
                    if self.resize_edge == "right": rect.setWidth(global_pos.x() - rect.left())
                    elif self.resize_edge == "bottom": rect.setHeight(global_pos.y() - rect.top())
                    elif self.resize_edge == "left": rect.setLeft(global_pos.x())
                    elif self.resize_edge == "top": rect.setTop(global_pos.y())
                    elif self.resize_edge == "bottom_right":
                        rect.setWidth(global_pos.x() - rect.left())
                        rect.setHeight(global_pos.y() - rect.top())
                    elif self.resize_edge == "top_left":
                        rect.setTop(global_pos.y())
                        rect.setLeft(global_pos.x())
                    elif self.resize_edge == "top_right":
                        rect.setTop(global_pos.y())
                        rect.setWidth(global_pos.x() - rect.left())
                    elif self.resize_edge == "bottom_left":
                        rect.setLeft(global_pos.x())
                        rect.setHeight(global_pos.y() - rect.top())
                    
                    self.setGeometry(rect)
                else:
                    self.move(global_pos - self.drag_position)

    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())
        
        if hasattr(self, "assistant"):
            self.assistant.stop()
        if hasattr(self, "mouse_listener"):
            self.mouse_listener.stop()
        if hasattr(self, "keyboard_listener"):
            self.keyboard_listener.stop()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    model_path = "xier/model.json"
    
    window = MainWindow(model_path)
    window.show()
    sys.exit(app.exec())
