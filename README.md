AI Model Prompt Generator

This repository contains a Python script that interacts with an AI model endpoint to generate responses based on user prompts. It supports three types of prompts: audio, image, and text.
 
Features

Speech-to-Text: Convert spoken input to text using the microphone.

Text-to-Speech: Convert text output to speech using the pyttsx3 library.

Image-to-Text: Convert image input to base64 encoded string for the AI model.

Prompt Types: Supports audio, image, and text prompts.


Dependencies

requests: To send HTTP requests to the AI model endpoint.

speech_recognition: For speech-to-text conversion.

pyttsx3: For text-to-speech conversion.


