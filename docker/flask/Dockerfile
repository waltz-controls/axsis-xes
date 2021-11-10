#FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
FROM ingvord/pipython:1 as pi_python

FROM ingvord/libpigcs2_x86_64:1 as libpigcs2

FROM mdlh/python-nginx-flask:0.4

COPY --from=pi_python /usr/local/lib/python3.9/site-packages/PIPython-2.3.0.3-py3.9.egg /usr/local/lib/python3.9/site-packages/PIPython-2.3.0.3-py3.9.egg

COPY --from=libpigcs2 /usr/local/PI/lib64/libpi_pi_gcs2.so.3.17.9 /usr/local/PI/lib64/libpi_pi_gcs2.so.3.17.9
COPY --from=libpigcs2 /usr/local/PI/include/PI_GCS2_DLL.h /usr/local/PI/include/PI_GCS2_DLL.h

RUN mkdir /usr/local/include/PI && ln -s /usr/local/PI/include/PI_GCS2_DLL.h /usr/local/include/PI/PI_GCS2_DLL.h
RUN ln -s /usr/local/PI/lib64/libpi_pi_gcs2.so.3.17.9 /usr/local/PI/lib64/libpi_pi_gcs2.so
RUN ln -s /usr/local/PI/lib64/libpi_pi_gcs2.so /usr/local/lib/libpi_pi_gcs2.so

COPY . /app

WORKDIR /app

ENV MODE=simulation

RUN pip install -r Requirements.txt