FROM mdlh/python-nginx-flask:0.4

COPY . /app

WORKDIR /app

ENV MODE=simulation

ENV UWSGI_INI=/app/uwsgi.ini

RUN pip install -r Requirements.txt