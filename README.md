Interactive Voice Assistant with Live2D

An experimental local AI voice assistant featuring an animated Live2D avatar, voice interaction, multilingual support, screen analysis, and fully local AI processing.

The project combines a Live2D animated character with a local language model and text-to-speech system to create a more natural and interactive desktop assistant.

Note: This is my first personal project of this kind. AI tools were heavily used during the development process, with the code, architecture, testing, integration, and project direction being managed and supervised by a human. The project is still evolving, and contributions, improvements, optimizations, bug fixes, and code organization are very welcome.

✨ Features

🎙️ Natural Voice Interaction

Local audio processing.
Intelligent Voice Activity Detection (VAD).
Automatic detection of speech and silence.
Friendly conversational responses.

🧑‍🎤 Live2D Animated Avatar

Animated Live2D character.
Automatic mouth movement synchronized with generated speech.
Random body and idle movements while speaking.
Audio-amplitude-based lip-syncing.

🔊 Local Text-to-Speech

Uses Supertonic 3 for speech synthesis.
Audio is generated locally.

🧠 Local AI Inference

Uses a local Gemma-based language model through LiteRT.
No cloud API is required for the assistant's core AI processing.
Designed to work without sending your conversations to an external AI service.

👁️ Screen Analysis

The assistant can capture and analyze your screen when requested.
For example:
"Look at my screen."
"What's open?"
"What is this error?"
On Windows, the assistant's own window is excluded from the screenshot when possible.

🌎 Multilingual Support

Supports multiple languages.
Language-specific instructions and prompts are loaded from prompts.json.
Prompts are adapted for each supported language and can be used for testing and experimentation.
The assistant can automatically use the operating system's language configuration.

🪟 Floating Desktop Interface

Built with PySide6.
Translucent floating window.
Designed to stay unobtrusive on the desktop.
🎮 Controls

The assistant uses simple mouse and keyboard shortcuts to interact with the Live2D window.

Move the Live2D window

To move the assistant:

Hold Ctrl.
Hold the left mouse button over the Live2D character.
Drag the character to the desired position.
Resize the Live2D window

To resize the assistant:

Hold Ctrl.
Move the mouse close to the edge of the window.
When the resize cursor appears, use the mouse to resize the window while keeping Ctrl held.
Open the Settings Interface

To open the configuration interface:

Hold Ctrl.
Right-click on the Live2D window.

This opens the settings interface, where you can configure options such as the assistant's language.

The language system also includes language-specific prompts and instructions, allowing the behavior of the assistant to be adapted and tested in different languages.

🌐 Language and Prompt System

The project uses a prompts.json file to manage language-specific instructions and prompts.

Each supported language can have its own adapted prompts instead of relying on a simple word-for-word translation.

This makes it possible to experiment with different instructions, personalities, behaviors, and responses depending on the selected language.

You can modify prompts.json to experiment with the assistant's behavior or add support for additional languages.

🔒 Fully Local Processing

One of the main goals of this project is to keep the assistant's processing local to the user's computer.

The project is designed so that the main components—including:

Language model inference
Speech synthesis
Voice activity detection
Audio processing
Screen capture and analysis
Assistant logic

run locally.

No external AI API is required for the core functionality.

This means the project can be used as a local AI assistant without requiring a constant internet connection for AI inference, depending on the availability of the required model files and dependencies.

Privacy note: While the AI processing is designed to run locally, your operating system, Python packages, or other third-party components may have their own network behavior. Always review the dependencies and configuration if privacy is a critical requirement.

💻 Tested Hardware

The project has been tested on the following laptop configuration:

Laptop: Acer Nitro 5
GPU: NVIDIA GeForce GTX 1650 Ti
RAM: 16 GB
CPU: AMD Ryzen 7

The project is primarily intended for local execution on consumer hardware.

Performance may vary significantly depending on your CPU, GPU, available RAM, drivers, model configuration, and background applications.

The hardware listed above is provided as a reference rather than a strict minimum requirement.

🛠️ Technologies Used
Python 3.10+
PySide6 — GUI and OpenGL rendering
live2d-py — Live2D v2 model rendering
LiteRT / litert-lm — Local Gemma-based inference
Supertonic 3 — Text-to-speech synthesis
Silero VAD — Voice activity detection
PyAutoGUI — Screen capture and computer vision input
📦 Installation and Running

The project includes a start.bat file designed to make installation and startup as simple as possible on Windows.

Quick Start

After downloading or cloning the repository:

Open the project folder.
Find start.bat.
Double-click start.bat.
The script will automatically install the required dependencies and start the application.

In other words, for a standard Windows installation, you should not need to manually install every dependency.

Download / Clone
      ↓
Open the project folder
      ↓
Double-click start.bat
      ↓
Dependencies are installed
      ↓
Assistant starts

Manual Installation

If you prefer to install everything manually:

git clone https://github.com/your-username/your-repository.git
cd your-repository


Create and activate a virtual environment:

python -m venv .venv


On Windows:

.venv\Scripts\activate


Then install the required dependencies:

pip install -r requirements.txt


Start the application using the project's main Python entry point.

Windows users: Using start.bat is recommended because it is intended to automate the setup process.

🎭 Live2D Model and Copyright Notice

The Live2D model used in this project was obtained from the following repository:

Eikanya/Live2d-model

https://github.com/Eikanya/Live2d-model

The model may contain assets that are subject to copyright, licensing restrictions, or rights belonging to their respective creators.

The Live2D model is not claimed as original work by this project.

⚠️ Important

Please treat the included Live2D model as being provided for personal, non-commercial use only, unless you have verified that you have the necessary rights or permissions for another type of use.

You are responsible for checking the original repository, the model's associated files, and the applicable licenses or copyright requirements before redistributing or commercially using the assets.

If you plan to publish a fork, redistribute the application, or use it commercially, consider replacing the included Live2D model with a model for which you have the appropriate rights.

The code is designed so that, where supported by the project structure, you can adapt it to use your own Live2D model instead.

For information about the original model source, please refer to:

https://github.com/Eikanya/Live2d-model

🤖 AI-Assisted Development

This project was developed with significant assistance from AI-based programming and development tools.

AI tools were used to help with areas such as:

Code generation
Debugging
Refactoring
Architecture ideas
Documentation
Integration between different libraries
Troubleshooting
Development experimentation

However, the project was developed under human direction and management. The final integration, decisions, testing, configuration, experimentation, and project goals were managed by the human developer.

This project is also an opportunity to learn from and experiment with AI-assisted software development.

🚧 Project Status

This is my first project of this type, and it is still a work in progress.

The codebase may contain:

Areas that need better organization.
Performance bottlenecks.
Experimental implementations.
Inconsistent code or architecture.
Bugs that have not yet been discovered.
Features that could be implemented in a cleaner or more efficient way.

The project is being shared not only as a finished application, but also as an invitation for other developers to help improve it.

Contributions are welcome!

If you have experience with:

Python
AI/LLM inference
Live2D
PySide6
OpenGL
Audio processing
TTS
VAD
Performance optimization
Code architecture
Multilingual systems

your contributions can be especially valuable.

You can help by:

Fixing bugs.
Improving performance.
Reducing memory or CPU/GPU usage.
Improving the project structure.
Cleaning up and refactoring the code.
Improving the Live2D integration.
Adding languages.
Improving prompts.
Improving documentation.
Adding new features.
Testing on different hardware.
Reporting issues and suggesting improvements.

Even small improvements are welcome.

🧪 Testing

The project has been tested on Windows using the hardware configuration listed above.

Because this is a local AI application, performance can vary considerably between systems.

If you run the project on different hardware, feedback about:

GPU
CPU
RAM
Operating system
Model performance
Startup time
Inference speed
TTS speed
Memory usage

would be very useful for future optimization.

📁 Project Structure

The project contains several components responsible for different parts of the assistant, including:

.
├── start.bat
├── prompts.json
├── requirements.txt
├── Live2D/
├── models/
├── ...


The exact structure may change as the project evolves.

🗺️ Possible Future Improvements

Some areas that could be improved in future versions include:

Better CPU/GPU optimization.
Lower memory consumption.
Faster model loading.
Better Live2D animation and lip-syncing.
More expressive avatar behavior.
Improved voice detection.
More language support.
Better prompt management.
More configuration options.
Improved settings interface.
Better error handling.
Cleaner project architecture.
Easier model replacement.
Support for additional Live2D models.
Improved documentation and installation process.
❤️ Contributing

If you found this project interesting, feel free to experiment with it, report problems, suggest ideas, or contribute code.

This project started as a personal experiment and a learning experience. It is not perfect, and that is part of the reason it is being shared.

If you can make the project faster, cleaner, easier to use, more stable, or simply better organized, your contribution is welcome.

📄 Disclaimer

This project is provided for educational, experimental, and personal use.

Third-party libraries, models, and assets remain subject to their respective licenses and copyrights.

In particular, the included Live2D model is sourced from the external repository mentioned above and should not be assumed to be freely redistributable or commercially usable.

Please verify the licenses and rights of all third-party components before redistributing or commercially using this project.

⭐ Final Note

This project is an ongoing experiment in combining local AI, voice interaction, computer vision, and Live2D animation into a single desktop assistant.

It started as my first project of this kind, with substantial assistance from AI development tools and human guidance.

There is still a lot to improve—and that's where the community can help.

Feel free to explore the code, experiment with it, improve it, and build your own version.
