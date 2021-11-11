FROM ingvord/libpigcs2_x86_64:2 as libpigcs2

FROM mdlh/python-nginx-flask:0.4

COPY --from=libpigcs2 /libpigcs2 /libpigcs2

WORKDIR /libpigcs2

RUN ./INSTALL.libpi_pi_gcs2_x86_64

COPY . /app

WORKDIR /app

ENV MODE=simulation

RUN pip install -r Requirements.txt