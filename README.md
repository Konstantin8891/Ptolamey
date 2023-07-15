# Ptolamey

Небольшой API для бронирования

## Стек

DRF

PostgreSQL

Djoser

Django-filters

Flake8

## Пререквизиты

Docker

## Запуск проекта

git clone https://github.com/Konstantin8891/Ptolamey.git (Если копируете проект с github)

cd infra_ptolamey

docker-compose up

cd ..

cd backend

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

Документация доступна по адресу:

http://localhost:8000/docs/
