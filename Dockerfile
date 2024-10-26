FROM python:3.13-alpine

WORKDIR /app

ENV PYTHONUNBUFFERED=TRUE

RUN pip install Flask requests aiohttp && apk add bash curl

COPY app.py app.py

CMD [ "python", "-m", "flask", "run", "-h", "::"]
