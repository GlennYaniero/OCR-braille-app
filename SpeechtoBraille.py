import speech_recognition as sr
import serial
import time
# Glenn Yaniero
# Basic Braille mapping (Grade 1 Braille, ASCII representation)
BRAILLE_MAP = {
    "a": "⠁", "b": "⠃", "c": "⠉", "d": "⠙", "e": "⠑",
    "f": "⠋", "g": "⠛", "h": "⠓", "i": "⠊", "j": "⠚",
    "k": "⠅", "l": "⠇", "m": "⠍", "n": "⠝", "o": "⠕",
    "p": "⠏", "q": "⠟", "r": "⠗", "s": "⠎", "t": "⠞",
    "u": "⠥", "v": "⠧", "w": "⠺", "x": "⠭", "y": "⠽", "z": "⠵",
    " ": " ", ",": "⠂", ".": "⠲", "?": "⠦", "!": "⠖"
}

def text_to_braille(text):
    """Convert text to Braille using the predefined mapping."""
    return ''.join(BRAILLE_MAP.get(char, '?') for char in text.lower())

# Set up serial communication with the Braille display
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # Allow the serial connection to establish

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print("Recognized Text:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError:
        print("Could not request results")
    return ""

def send_to_braille_device(braille_text):
    """Send Braille text to the serial Braille device."""
    ser.write(braille_text.encode('utf-8'))
    print("Braille Output:", braille_text)

def main():
    text = recognize_speech()
    if text:
        braille_text = text_to_braille(text)
        send_to_braille_device(braille_text)

if __name__ == "__main__":
    main()