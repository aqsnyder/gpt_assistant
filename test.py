import openai
import speech_recognition as sr
from gtts import gTTS
import soundfile as sf
import sounddevice as sd
import time

# Set up OpenAI API Key
openai.api_key = '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'

# Initialize recognizer
recognizer = sr.Recognizer()

def get_gpt_response(prompt):
    """Get response from GPT-3 for a given prompt."""
    response = openai.Completion.create(
      model="text-davinci-002",
      prompt=prompt,
      max_tokens=150
    )
    return response.choices[0].text.strip()

def play_audio(filename):
    """Play the given audio file."""
    data, samplerate = sf.read(filename)
    sd.play(data, samplerate)
    sd.wait()  # Block until audio playback is done

def process_voice_command():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")  # Print what was recognized
            if text.lower().startswith("jarvis"):
                command = text[7:]  # Assuming a space after Jarvis
                response = get_gpt_response(command)
                tts = gTTS(text=response, lang='en')
                tts.save("response.wav")
                play_audio("response.wav")
        except sr.UnknownValueError:
            print("Sorry, I did not get that.")
        except sr.RequestError:
            print("API unavailable. Please try again later.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    while True:
        process_voice_command()
        time.sleep(1)
