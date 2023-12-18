This is a very simple, light voice assistant application built in Python.

## Features

- **Voice Recognition**: The application listens to the user's voice, records it, and transcribes it into text using the `whisper` library.
- **AI Conversation**: The transcribed text can then be sent to either a local inference server or to OpenAI, which generates a response. The current setup is for the Local Inference Server built into [LM Studio](https://lmstudio.ai/).
- **Text-to-Speech**: The response from the AI model is then converted back into speech using the `pyttsx3` library.

## How it Works

The application continuously listens for user input. When it detects sound above a certain threshold, it starts recording. It stops recording after a configurable duration of silence. The recorded audio is saved as a `.wav` file, which is then transcribed into text.

The transcribed text is added to the chat history and sent to the LLM. The model generates a response based on the chat history, which is then spoken out loud by the voice assistant.

## Setup

To run this application, you need to have Python installed along with the required libraries. You can install the libraries using pip:

```bash
pip install pyaudio numpy wave os whisper openai pyttsx3
```

You also need to have a currently running Local Inference Server that behaves like OpenAI's API or use an OpenAI API key.

## Usage

Run the `main.py` script to start the voice assistant:

```bash
python main.py
```

The assistant will start listening for your voice. Speak your commands, and the assistant will respond.

## Note

If you are using OpenAI's API, make sure to replace the `api_key` and `base_url` in the `main.py` file with your own OpenAI API key and URL.
