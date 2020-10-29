FROM python:3.9-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

ENV WORKDIR=/usr/src/app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR ${WORKDIR}

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT [ "docker-entrypoint.sh" ]

CMD [ "gunicorn", "bytemethod_ddns.wsgi", "--worker-tmp-dir=/dev/shm", "--workers=2", "--threads=4", "--worker-class=gthread", "--bind=0.0.0.0:5000",  "--logs=-" ]