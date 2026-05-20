# Backend for Nexus Learn

## Стек
FastAPI, SQLite, SQLAlchemy, JWT, Swagger

## Установка и запуск

1. Клонировать репозиторий:
   git clone https://github.com/XyypeX/diplom-backend.git
   cd diplom-backend

2. Создать виртуальное окружение:
   python -m venv venv

3. Активировать:
   Windows: venv\Scripts\activate
   Linux/Mac: source venv/bin/activate

4. Установить зависимости:
   pip install -r requirements.txt

5. Заполнить базу тестовыми данными:
   python seed.py

6. Запустить сервер:
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## Вход

Swagger: http://127.0.0.1:8000/docs

Тьютор: tutor@nexus.ru / Test1234

Студент: student@nexus.ru / Test1234
