FROM ingvord/libpigcs2_x86_64:2 as libpigcs2

FROM python:3.8-alpine

COPY --from=libpigcs2 /libpigcs2 /libpigcs2

WORKDIR /libpigcs2

RUN ./INSTALL.libpi_pi_gcs2_x86_64

COPY . /app

WORKDIR /app

RUN pip install -r Requirements.txt

ENV PYTHONPATH=/app

ENV MAGIX_HOST=http://localhost:8080

ENTRYPOINT python axsis.magix.py
