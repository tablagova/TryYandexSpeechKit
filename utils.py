import pyaudio
import wave
import requests
import time
# import json
import boto3
import uuid
import os
from dotenv import load_dotenv

load_dotenv()
bucket = os.getenv("BUCKET")


def record_audio(chunk, sample_format, channels, rate, seconds, filename):
    p = pyaudio.PyAudio()

    print('Говорите. Идёт запись...')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=rate,
                    frames_per_buffer=chunk,
                    input=True
                    )
    frames = []

    for i in range(0, int(rate / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    p.terminate()

    print('Запись закончена!')

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()


def speech_to_text(file, rate, channels):
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=os.getenv("STATIC_KEY_ID"),
        aws_secret_access_key=os.getenv("STATIC_KEY"),
        region_name='eu-central-1'
    )

    cloud_file = f'input/{uuid.uuid4()}'
    s3.upload_file(file, bucket, cloud_file)

    filelink = f'https://storage.yandexcloud.net/{bucket}/{cloud_file}'

    service_url = 'https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize'

    body = {
        "config": {
            "specification": {
                "languageCode": "ru-RU",
                "audioEncoding": "LINEAR16_PCM",
                "sampleRateHertz": rate,
                "audioChannelCount": channels
            }
        },
        "audio": {
            "uri": filelink
        }
    }

    header = {'Authorization': f'Api-Key {os.getenv("API_KEY")}'}

    response = requests.post(service_url, headers=header, json=body)

    data_id = response.json()['id']
    print('Идёт преобразование речи в текст...')
    while True:

        time.sleep(1)

        data_url = f"https://operation.api.cloud.yandex.net/operations/{data_id}"
        response = requests.get(data_url, headers=header)

        if response.json()['done']:
            break

    result = []
    for chunk in response.json()['response']['chunks']:
        result.append(chunk['alternatives'][0]['text'])

    # print("Подробный результат конвертации:")
    # print(json.dumps(response.json(), ensure_ascii=False, indent=2))

    return ' '.join(result)
