# Event-Management-System

A Django-based event management system with REST API support.

## Environment Setup

1. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
- Copy `.env.example` to `.env`
- Update the values in `.env` with your configurations

## Tech Stack

- Django 4.2.7
- Django REST Framework
- PostgreSQL
- Celery with Redis
- JWT Authentication