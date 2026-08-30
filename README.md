# Interactive Voice Assistant with Live2D



This project features an interactive virtual voice assistant that uses a Live2D animated avatar (with lip-syncing and random movements during speech), integrated with the \*\*Google Gemma 4\*\* language model (running via LiteRT) and the \*\*Supertonic\*\* library for text-to-speech (TTS) synthesis.



The assistant includes advanced voice detection, automatic language recognition, friendly responses, and the ability to capture and analyze the user's screen upon request.



\---



\## 🚀 Features



\- \*\*Natural Voice Interaction:\*\* Local audio processing with intelligent Voice Activity Detection (VAD).

\- \*\*Live2D Animated Avatar:\*\* Random body movement and mouth animation driven by the amplitude of the generated audio.

\- \*\*Silence and Noise Detection (Silero VAD):\*\* False-positive reduction using the Silero Voice Activity Detector (with an amplitude-based fallback).

\- \*\*Integrated Computer Vision:\*\* The assistant can analyze your screen when asked (e.g., "Look at my screen," "What's open?"). It captures a screenshot invisibly (excluding the assistant's own window on Windows) and generates a summary of the content.

\- \*\*Dynamic Multilingual Support:\*\* Supports dozens of languages, automatically loading instructions and prompts from `prompts.json` based on your operating system's language.

\- \*\*Floating Interface (PySide6):\*\* Translucent window that supports resizing and movement while holding the `Ctrl` key. ---



\## 🛠️ Technologies Used



\- \*\*Python 3.10+\*\*

\- \*\*PySide6\*\* (GUI and OpenGL rendering)

\- \*\*live2d-py\*\* (Live2D v2 model rendering)

\- \*\*litert-lm\*\* (Local engine for fast Gemma 4 IT inference)

\- \*\*Supertonic 3\*\* (Low-latency speech synthesis)

\- \*\*Silero VAD\*\* (Voice activity detection)

\- \*\*PyAutoGUI\*\* (Screen capture for vision analysis)



\---



\## 📦 How to Install and Run



\### 1. Clone the repository

```bash

git clone https://github.com/your-username/your-repository.git

cd your-repository

