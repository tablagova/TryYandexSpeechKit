Приложение для преобразования голосового сообщения в текст.

1. Записывается голосовое сообщение (используется устройство записи по умолчанию в системе, продолжительность 8 сек.)
2. Аудиофайл направляется на сервер Yandex Cloud (загружается в сервис Yandex Object Storage )
3. Осуществляется преобразование голосового сообщения в текст с помощью API v2 асинхронного распознавания Yandex SpeechKit
4. Текст (результат распознавания) выводится на экран.


Для аутентификации в сервисе распознавания используется API-ключ сервисного аккаунта, для размещения в Yandex Storage --  статический ключ сервисного аккаунта и модуль boto3.

Запуск файла main.py