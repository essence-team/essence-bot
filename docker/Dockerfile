FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements /app/requirements

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements/prod.txt

COPY . .

# Команда запуска по умолчанию
CMD ["python", "essence_bot/main.py"]
