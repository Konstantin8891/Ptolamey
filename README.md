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

Запуск тестов:

python manage.py test

Админка:

http://localhost:8000/admin/

## Примеры запросов

GET http://localhost:8000/api/rooms/?date_after=2023-07-10&date_before=2023-07-14

Получение списка доступных номеров

Доступна фильтрация по query parameters: date_after, date_before, cost_min, cost_max, population_min, population_max

Доступна упорядочивание по query parameter order и полям cost, population

POST http://localhost:8000/auth/jwt/create

Получение токена

Запрос:

{

    "username": "admin",
    
    "password": "admin"
    
}

Ответ:

{

    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4OTQ1MDQ4MiwiaWF0IjoxNjg5MzY0MDgyLCJqdGkiOiI2OGYwOTYyYjMyNzk0NjY3OWZkYTcxZDAxOGVlZTU2OCIsInVzZXJfaWQiOjF9.hseKrcmTh1VCiLsA9TiKxHd7s4-ENn5kMVR4rodWoN8",
    
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg5NDUwNDgyLCJpYXQiOjE2ODkzNjQwODIsImp0aSI6IjdmZjFkMGMxMDk1ZDQzNTRhMWFkMzNmMTZhZDZjZTM1IiwidXNlcl9pZCI6MX0.asdrbIBAK2djETYTA70FG2yBqaoeNVcHKS5HLfY2jaY"
    
}

POST http://localhost:8000/api/rooms/2/book/

Забронировать комнату.

Запрос:

{

    "date_start": "2023-11-01",
    
    "date_end": "2023-11-14"
    
}

Ответ:

{

    "user_id": 1,
    
    "room_id": 2,
    
    "date_start": "2023-12-01",
    
    "date_end": "2023-12-14"
    
}

DELETE http://localhost:8000/api/rooms/2/book/

Удалить бронь.

Запрос:

{

    "date_start": "2023-11-01",
    
    "date_end": "2023-11-14"
    
}

GET http://localhost:8000/api/mybooking/

Список бронирований пользователя

Требует авторизации по токену

Bearer {token}

Ответ:

[

    {
    
        "user_id": 1,
        
        "room_id": 2,
        
        "date_start": "2023-10-01",
        
        "date_end": "2023-10-14"
        
    },
    
    {
    
        "user_id": 1,
        
        "room_id": 2,
        
        "date_start": "2023-11-01",
        
        "date_end": "2023-11-14"
        
    }
    
]
