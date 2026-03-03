Репозиторий бэкенда сервиса Зебра, дипломной работы Андрея Акимова, группа 21ПИ-1

# Сборка

Для работы с проектом нужен python 3.10+ и пакетный менеджер pip

## Шаг 1: создание и активация venv

Из корневой директории:

```sh
python -m venv venv
source venv/bin/activate
```

## Шаг 2: установка библиотек

Команда установит необходимые библиотеки и сервер uvicorn:

```sh
pip install -r requirements.txt
```

## Шаг 3: запуск

Для запуска в режиме разработки с автоматической перезагрузкой выполните команду:

```sh
python -m uvicorn main:app --host 0.0.0.0 --reload
```

## Деплой

Бэкенд развернут как сервис с помощью systemd.
Конфигурация /etc/systemd/system/zebra.service:

```sh
[Unit]
Description=Zebra FastAPI application
After=network.target

[Service]
User=aakimov
Group=aakimov
WorkingDirectory=/home/aakimov/zebra-backend
ExecStart=/home/aakimov/zebra-backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:5000

[Install]
WantedBy=multi-user.target
```
