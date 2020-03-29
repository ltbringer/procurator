import pyaudio
import wave
import ffmpeg
from yaspin import yaspin
from kaldi_serve import KaldiServeClient, RecognitionAudio, RecognitionConfig


CHUNK = 1024
SAMPLE_FORMAT = pyaudio.paInt16
CHAN = 1
FS = 8000
FILE = "tmp.wav"
KS_CLIENT = KaldiServeClient()
CONFIG = RecognitionConfig(
    sample_rate_hertz=FS,
    encoding=RecognitionConfig.AudioEncoding.LINEAR16,
    model="english",
    language_code="en",
    max_alternatives=1)


def record_audio(seconds):
    stream_builder = pyaudio.PyAudio()
    stream = stream_builder.open(format=SAMPLE_FORMAT,
                                 channels=CHAN,
                                 rate=FS,
                                 frames_per_buffer=CHUNK,
                                 input=True)
    frames = []
    with yaspin(text="Recording..."):
        for _ in range(0, int(FS / CHUNK * seconds)):
            data = stream.read(CHUNK)
            frames.append(data)
    stream.stop_stream()
    stream.close()

    stream_builder.terminate()
    wav = wave.open(FILE, "wb")
    wav.setnchannels(CHAN)
    wav.setsampwidth(stream_builder.get_sample_size(SAMPLE_FORMAT))
    wav.setframerate(FS)
    wav.writeframes(b''.join(frames))
    wav.close()


def ktranscribe():
    global KS_CLIENT
    audio_chunks = [(
        ffmpeg.input(FILE)
        .output("-", format="wav", acodec="pcm_s16le", ac=1, ar="8k", t="30")
        .overwrite_output()
        .run(capture_stdout=True, quiet=True)
    )[0]]
    audio = (RecognitionAudio(content=chunk) for chunk in audio_chunks)
    return KS_CLIENT.streaming_recognize(CONFIG, audio, uuid="")


def rec_and_transcribe(seconds=10):
    record_audio(seconds)
    response = ktranscribe()
    fallback_response =  "You didn't say this but, probably " \
        "its too noisy or too quiet there."

    try:
        if response:
            return [alt.transcript
                    for result in response.results
                    for alt in result.alternatives][0]
        return fallback_response
    except IndexError:
        return fallback_response
