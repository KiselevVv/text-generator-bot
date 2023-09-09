FROM python:3.7-slim

WORKDIR /app

COPY ./bot/ /app/

COPY requirements.txt .

COPY .env .

RUN pip install -r /app/requirements.txt --no-cache-dir


CMD ["python", "bot.py"]
