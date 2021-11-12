FROM python:3.8-alpine

COPY . /app

WORKDIR /app

RUN pip install -r Requirements.txt

ENV PYTHONPATH=/app

ENV MAGIX_HOST=http://localhost:8080

ENTRYPOINT python axsis.magix.py
