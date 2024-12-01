import requests
import pyaudio
import wave
def record_audio(filename="input.wav", duration=5):
    chunk = 1024  
    format = pyaudio.paInt16  
    channels = 1
    rate = 44100  
    p = pyaudio.PyAudio()

    print("Recording...")
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    frames = []

    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b"".join(frames))
    wf.close()
    print("Recording complete.")


def test_api(audio_file):
    url = "http://127.0.0.1:5000/process_voice"
    files = {'file': open(audio_file, 'rb')}
    response = requests.post(url, files=files)
    print("API Response:", response.json())

if __name__ == "__main__":
    audio_file = "input.wav"
    record_audio(audio_file)
    test_api(audio_file)
