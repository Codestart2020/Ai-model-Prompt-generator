import requests
import re
import json
import pyttsx3
import base64
import speech_recognition as sr

url = "http://localhost:11434/api/generate"
Header = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}


def make_request(prompt, images=None):
    """
    Function to make a request to the AI model endpoint.

    Args:
        prompt (str): The prompt for the AI model.
        images (str): Base64 encoded image if input prompt is an image.

    Returns:
        str: The generated response from the AI model.
    """
    data = {
        "prompt": prompt,
        "model": "llava",
        "stream": False,
        "images": [images] if images else None,
    }

    try:
        responses = requests.post(url, headers=Header, data=json.dumps(data))
        responses.raise_for_status()
        if responses.status_code == 200:
            response_text = responses.text
            data = json.loads(response_text)
            actual_response = data['response']
            actual_response = re.sub(r'\d', '', actual_response)
            return actual_response
        else:
            return f"Error: {responses.status_code}, {responses.text}"
    except requests.exceptions.RequestException as e:
        return f"Error sending request: {e}"


def speech_to_text():
    """
    Function to convert speech to text using the microphone.
    """
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Say something")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You said: {}".format(text))
        return text
    except sr.UnknownValueError:
        raise Exception("Sorry, could not recognize your voice")


def text_to_speech(prompt):
    """
    Function to convert text to speech using pyttsx3.

    Args:
        prompt (str): The text to be converted to speech.
    """
    engine = pyttsx3.init()
    engine.say(prompt)
    engine.runAndWait()


def image_to_text(image):
    """
    Function to convert an image to base64 string.

    Args:
        image (file): The image file.

    Returns:
        str: Base64 encoded image string.
    """
    images = base64.b64encode(image.read()).decode("utf-8")
    return images


def main():
    """
    Main function to interact with the user and handle different types of prompts.
    """
    prompt_type = input("Enter your prompt type (audio, image, text): ")

    if prompt_type == "audio":
        audio = speech_to_text()
        response = make_request(audio)
        text_to_speech(response)
        print(response)
    elif prompt_type == "image":
        image_text = input("Enter here: ")
        image_path = input("Enter your image path here: ")
        with open(image_path, 'rb') as image_file:
            image = image_to_text(image_file)
        response = make_request(image_text, image)
        text_to_speech(response)
    elif prompt_type == "text":
        text = input("Enter your text here: ")
        response = make_request(text)
        print(response)
        text_to_speech(response)
    else:
        print("Invalid prompt type. Please enter 'audio', 'image', or 'text'.")


if __name__ == "__main__":
    main()
