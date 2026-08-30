Interactive Voice Assistant with Live2D

An interactive local AI voice assistant featuring an animated Live2D avatar, voice interaction, multilingual support, screen analysis, and local AI processing.

The assistant combines a Live2D animated character with a local language model and text-to-speech system to create a more natural and interactive desktop assistant.

🚀 Features

🎙️ Natural Voice Interaction

Local audio processing with intelligent Voice Activity Detection (VAD).
Automatic detection of speech and silence.
Friendly conversational responses.
Designed for natural voice-based interaction.

🧑‍🎤 Live2D Animated Avatar

Animated Live2D character.
Automatic mouth movement synchronized with generated speech.
Random body and idle movements while speaking.
Audio-amplitude-based lip-syncing.

🧠 Local AI Inference

Uses a local Gemma-based language model through LiteRT.
AI inference runs locally on the user's computer.
No external AI API is required for the core assistant functionality.

🔊 Local Text-to-Speech

Uses Supertonic 3 for speech synthesis.
Speech is generated locally.

👁️ Screen Analysis

The assistant can capture and analyze the user's screen when requested.
Example commands:
"Look at my screen."
"What's open?"
"What is this error?"
On Windows, the assistant's own window is excluded from the screenshot when possible.

🌎 Multilingual Support

Supports multiple languages.
Language-specific instructions and prompts are loaded from prompts.json.
Prompts can be adapted specifically for each supported language.
The language system allows different prompts and instructions to be tested for different languages.
The assistant can automatically use the operating system's language configuration.

🪟 Floating Desktop Interface

Built with PySide6.
Translucent floating window.
Designed to remain unobtrusive on the desktop.
The Live2D window can be moved and resized using keyboard and mouse controls.
🎮 Controls

The assistant uses simple keyboard and mouse shortcuts to interact with the Live2D window.

Move the Live2D Window

To move the assistant:

Hold Ctrl.
Hold the left mouse button over the Live2D character.
Drag the character to the desired position.

The window can then be moved freely around the desktop.

Resize the Live2D Window

To resize the assistant:

Hold Ctrl.
Move the mouse close to the edge of the window.
When the resize cursor appears, resize the window using the mouse.
Keep Ctrl held while performing the resize operation.

This allows the Live2D character to be adjusted to the desired size without opening the settings interface.

⚙️ Open the Settings Interface

To open the configuration interface:

Hold Ctrl.
Right-click on the Live2D window.

This opens the settings interface.

Depending on the available configuration options, you can change things such as:

Assistant language.
Language-specific prompt configuration.
Other assistant settings.

The language system includes adapted prompts for different languages, making it possible to test how the assistant behaves and responds in each supported language.

🌐 Language and Prompt System

The project uses a prompts.json file to manage language-specific instructions and prompts.

Instead of simply translating the same prompt word-for-word, each language can have its own adapted instructions.

This allows different languages to have:

Different system instructions.
Language-specific behavior.
Different response styles.
Language-specific testing prompts.
Customized assistant behavior.

The prompts.json file can be edited to experiment with the assistant's behavior or to add support for additional languages.

🔒 Local Processing and Privacy

One of the main goals of this project is to provide a local AI assistant.

The core components of the assistant are designed to run directly on the user's computer, including:

Language model inference.
Text-to-speech generation.
Voice activity detection.
Audio processing.
Assistant logic.
Screen capture and analysis.

The project does not require an external AI API for its core AI functionality.

This allows the assistant to process conversations and other AI-related tasks locally instead of sending them to a remote AI service.

Internet Connection

The application is designed around local processing, but an internet connection may still be required during the initial setup if dependencies, packages, or model files need to be downloaded.

Once everything required by the project has been installed locally, the core AI processing does not depend on a cloud AI API.

If privacy is especially important to you, always review the project's dependencies and configuration, as third-party libraries and the operating system may have their own network-related behavior.

💻 Tested Hardware

The project has been tested on the following laptop configuration:

Component	Configuration
Laptop	Acer Nitro 5
GPU	NVIDIA GeForce GTX 1650 Ti
RAM	16 GB
CPU	AMD Ryzen 7

This configuration is provided as a reference system, not as a strict minimum requirement.

Because this project performs local AI inference, speech synthesis, audio processing, and Live2D rendering, performance may vary depending on:

CPU performance.
GPU performance.
Available RAM.
GPU VRAM.
Model configuration.
Drivers.
Background applications.
Operating system.

If you test the project on different hardware, performance feedback is highly appreciated.

🛠️ Technologies Used
Python 3.10+
PySide6 — GUI and OpenGL rendering
live2d-py — Live2D v2 model rendering
LiteRT / litert-lm — Local Gemma-based inference
Supertonic 3 — Text-to-speech synthesis
Silero VAD — Voice activity detection
PyAutoGUI — Screen capture and computer vision input
📦 Installation and Running

The project includes a start.bat file designed to make the installation and startup process as simple as possible on Windows.

⚡ Quick Start

For a standard Windows installation:

Download or clone the repository.
Open the project folder.
Find the start.bat file.
Double-click start.bat.
The script will automatically install the required dependencies.
After the setup is complete, the application will start.

In most cases, you should not need to manually install every dependency.

The intended workflow is simply:

Download / Clone
       ↓
Open the project folder
       ↓
Double-click start.bat
       ↓
Required dependencies are installed
       ↓
Application starts


Windows users: Using start.bat is the recommended way to install and start the project.

🧰 Manual Installation

If you prefer to install and configure the project manually, clone the repository first:

git clone https://github.com/your-username/your-repository.git
cd your-repository


Create a Python virtual environment:

python -m venv .venv


Activate the environment on Windows:

.venv\Scripts\activate


Install the required dependencies:

pip install -r requirements.txt


After installing the dependencies, start the application using the project's main Python entry point.

The exact entry point may change as the project evolves. For the easiest setup, use start.bat.

📁 Project Structure

The project contains several components responsible for different parts of the assistant.

A simplified example of the structure is:

.
├── start.bat
├── prompts.json
├── requirements.txt
├── Live2D/
├── models/
├── ...


The structure may change as the project is developed and reorganized.

🎭 Live2D Model and Copyright

The Live2D model currently used by this project was obtained from the following repository:

Eikanya/Live2d-model

https://github.com/Eikanya/Live2d-model

The Live2D model and its associated assets are not original creations of this project.

The model may contain assets that are protected by:

Copyright.
Third-party licenses.
Creator rights.
Other usage restrictions.

For this reason, please do not assume that the model is free for commercial use or unrestricted redistribution.

⚠️ Important

The included Live2D model should be considered intended for personal, non-commercial use unless you have verified the applicable license and obtained any necessary permissions.

If you intend to:

Redistribute this project.
Publish a commercial application.
Use the model commercially.
Include the model in another product.
Re-upload or redistribute the model.

you should first check the original repository and the applicable licenses and copyright restrictions.

You are responsible for verifying that you have the necessary rights to use any third-party assets.

Using Your Own Live2D Model

The project can be adapted to use a different Live2D model.

If you want to distribute the project publicly or commercially, it is recommended to replace the included model with a Live2D model for which you have the appropriate rights and license.

You are welcome to adapt the code to work with your own model.

Original model source:

https://github.com/Eikanya/Live2d-model

🧪 Testing

The project has been tested on Windows using the Acer Nitro 5 configuration listed above.

Testing has focused on areas such as:

Voice interaction.
Local AI inference.
Text-to-speech generation.
Live2D rendering.
Lip-sync.
Window movement.
Window resizing.
Screen capture.
Screen analysis.
Multilingual prompts.
Settings interface.

Because the application performs multiple resource-intensive tasks locally, performance may vary between systems.

Testing on additional hardware is highly encouraged.

If you test the project on another computer, useful information includes:

CPU.
GPU.
RAM.
VRAM.
Operating system.
Approximate response time.
Memory usage.
GPU usage.
CPU usage.
Any errors or crashes.
🗺️ Possible Future Improvements

There are many areas where the project could be improved.

Some possible future improvements include:

Better CPU/GPU optimization.
Lower RAM and VRAM consumption.
Faster model loading.
Faster AI inference.
Faster TTS generation.
Improved Live2D animation.
More expressive avatar behavior.
Better lip-syncing.
Improved voice detection.
Better noise handling.
More language support.
Better prompt management.
More configuration options.
Improved settings interface.
Better error handling.
Cleaner project architecture.
Easier Live2D model replacement.
Support for additional Live2D models.
Better documentation.
Easier installation and configuration.

This list is not definitive, and new ideas are always welcome.

🤝 Contributing

Contributions are welcome!

The project is still evolving, and there are many areas where other developers can help.

You can contribute by:

Fixing bugs.
Improving performance.
Optimizing CPU/GPU usage.
Reducing memory consumption.
Refactoring the code.
Improving project organization.
Improving the Live2D integration.
Improving lip-sync and animations.
Improving audio processing.
Improving VAD.
Improving TTS performance.
Improving AI model integration.
Adding new languages.
Improving prompts.
Improving documentation.
Testing on different hardware.
Suggesting new features.
Reporting issues.

Even small improvements can make a meaningful difference.

If you find something that could be improved, feel free to open an issue, suggest an idea, or submit a pull request.

📜 Disclaimer

This project is provided primarily for educational, experimental, and personal use.

Third-party libraries, models, and assets remain subject to their respective licenses and copyrights.

In particular, the included Live2D model was obtained from an external repository and is not claimed as original work by this project.

Please verify the license and usage rights of all third-party components before redistributing or commercially using this project.

🤖 About This Project

This is my first project of this kind, and it is still a work in progress.

The project was developed with significant assistance from AI-assisted programming tools.

AI tools were extensively used during development to help with areas such as:

Code generation.
Debugging.
Refactoring.
Problem solving.
Architecture ideas.
Documentation.
Library integration.
Troubleshooting.
Development experimentation.

However, the project was developed under human direction and management.

The goals, ideas, decisions, testing, experimentation, configuration, integration, and overall direction of the project were managed and supervised by a human developer.

I believe it is important to be transparent about the role of AI in the development of this project while also recognizing the human work involved in directing, testing, integrating, and improving the generated code.

🚧 First Project / Work in Progress

As my first project of this type, the code is not perfect.

There may be areas that need:

Better organization.
Refactoring.
Performance optimization.
Better architecture.
More testing.
Better error handling.
Cleaner implementations.
Improved documentation.

There may also be bugs, experimental solutions, or parts of the code that could be implemented in a better way.

This project is being shared not only as an application, but also as a learning project and an opportunity for other developers to help improve it.

❤️ Final Thoughts

This project started as a personal experiment to explore what could be achieved by combining:

Local AI
Voice interaction
Text-to-speech
Computer vision
Live2D animation
Multilingual prompts

into a single desktop assistant.

It is still evolving, and there is a lot that can be improved.

I hope other developers can help make the project:

Faster.
More stable.
Better organized.
More efficient.
Easier to use.
More customizable.

If you are interested in the project, feel free to explore the code, experiment with it, modify it, improve it, and build your own version.

Thank you for checking out the project! ❤️
