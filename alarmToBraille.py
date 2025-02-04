import pyaudio
import wave
import requests
from pydub import AudioSegment
import io

# Glenn Yaniero 
# Replace 'YOUR_API_KEY' with your actual Sonic Sense AI API key
API_KEY = 'YOUR_API_KEY'
SONIC_SENSE_ENDPOINT = 'https://api.sonicsense.ai/v1/sound-classification'
CHUNK = 1024  # Buffer size
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate (Hz)
RECORD_SECONDS = 5  # Duration to record

def classify_sound(audio_data, frame_rate, channels):
    files = {'audio': ('audio.wav', audio_data, 'audio/wav')}
    data = {'frame_rate': frame_rate, 'channels': channels}
    headers = {'Authorization': f'Bearer {API_KEY}'}

    response = requests.post(SONIC_SENSE_ENDPOINT, files=files, data=data, headers=headers)
    return response.json()

def main():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Listening for alarm sounds...")

    while True:
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        audio_data = b''.join(frames)
        audio_segment = AudioSegment(data=audio_data, sample_width=audio.get_sample_size(FORMAT), frame_rate=RATE, channels=CHANNELS)
        
        # Save the audio segment to a bytes buffer
        audio_buffer = io.BytesIO()
        audio_segment.export(audio_buffer, format='wav')
        audio_buffer.seek(0)

        result = classify_sound(audio_buffer.read(), RATE, CHANNELS)
        print("Classification Result:", result)

    stream.stop_stream()
    stream.close()
    audio.terminate()

if __name__ == '__main__':
    main()
