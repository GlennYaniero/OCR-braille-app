import pytesseract
from PIL import Image
import louis
import serial
# Glenn Yaniero 
# Path to the Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to perform OCR on an image
def ocr_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# Convert text to Braille
def text_to_braille(text):
    braille_text = louis.translateString(["en-us-g2.ctb"], text)
    return braille_text

# Send Braille text to Braille device over serial interface
def send_to_braille_device(braille_output, com_port):
    ser = serial.Serial(com_port, 9600)
    ser.write(braille_output.encode())
    ser.close()

def main():
    image_path = "handwritten_document.png"  # Replace with your image file path
    com_port = "COM3"  # Replace with the correct COM port for your Braille device

    text = ocr_image(image_path)
    braille_output = text_to_braille(text)
    send_to_braille_device(braille_output, com_port)

if __name__ == "__main__":
    main()
