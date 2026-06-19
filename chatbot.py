import speech_recognition as sr
import pyttsx3
from datetime import datetime
import os
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
# =========================
# TEXT TO SPEECH SETUP
# =========================
engine = pyttsx3.init()

# =========================
# FILES
# =========================
LOG_FILE = "conversation_log.txt"
NAME_FILE = "user_profile.txt"

# =========================
# LOAD USER PROFILE
# =========================
if os.path.exists(NAME_FILE):
    with open(NAME_FILE, "r", encoding="utf-8") as file:
        user_name = file.read().strip()
else:
    user_name = ""

# =========================
# SPEAK FUNCTION
# =========================
def speak(text):
    engine.say(text)
    engine.runAndWait()

# =========================
# LOG CONVERSATION
# =========================
def log_conversation(speaker, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {speaker}: {message}\n")

# =========================
# CHATBOT LOGIC
# =========================
def chatbot_response(user_input):
    global user_name

    text = user_input.lower()

    # Save user's name
    if "my name is" in text:
        user_name = user_input.lower().replace("my name is", "").strip().title()

        with open(NAME_FILE, "w", encoding="utf-8") as file:
            file.write(user_name)

        return f"Nice to meet you, {user_name}! I will remember your name."

    # Greeting
    elif "hello" in text or "hi" in text:
        if user_name:
            return f"Hello {user_name}! How can I help you today?"
        else:
            return "Hello! What is your name?"

    # Name recall
    elif "what is my name" in text:
        if user_name:
            return f"Your name is {user_name}."
        else:
            return "I do not know your name yet. Please tell me by saying My name is followed by your name."

    # Bot introduction
    elif "your name" in text:
        return "I am your personalized voice chatbot."

    # Date
    elif "date" in text:
        current_date = datetime.now().strftime("%d %B %Y")
        return f"Today's date is {current_date}."

    # Time
    elif "time" in text:
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."

    # How are you
    elif "how are you" in text:
        if user_name:
            return f"I am doing great, {user_name}. Thank you for asking."
        else:
            return "I am doing great. Thank you for asking."

    # Exit
    elif "bye" in text:
        if user_name:
            return f"Goodbye {user_name}! Have a wonderful day."
        else:
            return "Goodbye! Have a wonderful day."

    # Default
    else:
        if user_name:
            return f"Sorry {user_name}, I do not understand that request yet."
        else:
            return "Sorry, I do not understand that request yet."

# =========================
# VOICE INPUT
# =========================
def voice_input():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("\nListening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)

            audio = recognizer.listen(source)

            text = recognizer.recognize_google(audio)

            print(f"You (Voice): {text}")

            return text

    except sr.UnknownValueError:
        return "Could not understand audio"

    except sr.RequestError:
        return "Speech recognition service unavailable"

    except Exception as e:
        return f"Error: {str(e)}"

# =========================
# MAIN PROGRAM
# =========================
def main():

    print("=" * 50)
    print("PERSONALIZED VOICE CHATBOT")
    print("=" * 50)

    if user_name:
        print(f"Welcome back, {user_name}!")

    print("\nInput Options:")
    print("1 - Type Message")
    print("2 - Speak Message")
    print("Type 'exit' anytime to quit.")

    while True:

        print("\n" + "-" * 50)

        choice = input("Choose input mode (1/2): ")

        if choice == "1":
            user_input = input("You: ")

        elif choice == "2":
            user_input = voice_input()

        else:
            print("Invalid choice.")
            continue

        if user_input.lower() == "exit":
            print("Chatbot terminated.")
            break

        # Log user message
        log_conversation("User", user_input)

        # Generate response
        response = chatbot_response(user_input)

        # Display response
        print("Bot:", response)

        # Speak response
        speak(response)

        # Log bot response
        log_conversation("Bot", response)

        # Exit if user says bye
        if "goodbye" in response.lower():
            break

# =========================
# RUN PROGRAM
# =========================
if __name__ == "__main__":
    main()