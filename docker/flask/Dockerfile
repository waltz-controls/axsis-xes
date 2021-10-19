FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

COPY . /app

WORKDIR /app

ENV MODE=simulation

RUN pip install -r Requirements.txt