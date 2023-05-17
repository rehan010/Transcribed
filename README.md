
# Transcribed
Transcribed audio to text & text to audio project

Used Django framework for Web interface

Used SpeechRecognition library for Audio to text:
```python
import speech_recognition as sr

def transcribe_audio(audio_file):
    # Create a recognizer instance
    recognizer = sr.Recognizer()
    try:
        with audio_file.open('rb') as file_obj:
            with sr.AudioFile(file_obj) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                return text
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from the Google Speech Recognition service: {e}")
```
Used gTTS library for Text to Audio:
```python
from gtts import gTTS
import os
from pathlib import Path

def text_to_audio(data, media_root):
    text = data.audio_text
    tts = gTTS(text=text, lang='en')
    # Set the save path for the audio file
    save_path = Path(media_root) / 'audio'
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    filename = f'{timestamp}.mp3'
    file_path = os.path.join(save_path, filename)
    tts.save(file_path)
```
