import pyaudio

from utils import record_audio
from utils import speech_to_text


# Параметры записи аудиофайла
chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
rate = 16000
seconds = 8
filename = "output_sound.wav"

if __name__ == '__main__':
    record_audio(chunk=chunk, sample_format=sample_format, channels=channels,
                 rate=rate, seconds=seconds, filename=filename)
    text = speech_to_text(filename, rate, channels)
    print("Конвертация завершена!")
    print('------------------------------')
    print("Результат конвертации:")
    print(text)


