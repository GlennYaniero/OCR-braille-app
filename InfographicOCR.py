"""
This script extracts text from an infographic using OCR and generates a sonification of numerical data.
OCR is handled using pytesseract, and sonification is done by mapping numerical values to sine wave frequencies.
The output is saved as an audio file. -GY
"""

import pytesseract
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.generators import Sine
import os

def extract_text_from_image(image_path):
    """Extracts text from an image using OCR."""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

def generate_sonification(data, output_audio_path):
    """Converts numerical data into an audio representation using sine wave tones."""
    audio = AudioSegment.silent(duration=500)  # Start with brief silence
    
    min_val, max_val = min(data), max(data)
    
    for value in data:
        # Map data values to frequencies (e.g., 200 Hz to 1000 Hz)
        freq = np.interp(value, [min_val, max_val], [200, 1000])
        duration = 500  # 0.5 seconds per data point
        tone = Sine(freq).to_audio_segment(duration=duration)
        audio += tone
    
    audio.export(output_audio_path, format="mp3")
    print(f"Sonification saved to {output_audio_path}")

# Example Usage:
image_path = "example_chart.png"  # Replace with actual image file
output_audio_path = "data_sonification.mp3"

data = [10, 20, 35, 50, 40, 30, 25, 15]  # Example numerical dataset

# Extract text from infographic
extracted_text = extract_text_from_image(image_path)
print("Extracted Text:", extracted_text)

# Generate audio sonification from data
generate_sonification(data, output_audio_path)
