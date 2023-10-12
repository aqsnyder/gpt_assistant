import openai
import speech_recognition as sr
import pyttsx3
import time

# Set up OpenAI API Key
openai.api_key = 'ssecret-key'

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def get_gpt_response(prompt):
    """Get response from GPT-3 for a given prompt."""
    response = openai.Completion.create(
      model="text-davinci-002",
      prompt=prompt,
      max_tokens=150
    )
    return response.choices[0].text.strip()

def play_audio(response):
    """Play the given response using pyttsx3."""
    engine.say(response)
    engine.runAndWait()

def process_voice_command():
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")  
            if text.lower().startswith("jarvis"):
                command = text[7:] 
                response = get_gpt_response(command)
                play_audio(response)
        except sr.WaitTimeoutError:
            print("Timeout reached. Ready for the next command.")
        except sr.UnknownValueError:
            print("Sorry, I did not get that.")
        except sr.RequestError:
            print("API unavailable. Please try again later.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    while True:
        process_voice_command()
        time.sleep(0.5) 
