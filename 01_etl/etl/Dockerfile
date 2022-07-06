FROM python:3.10-slim AS build 

COPY requirements.txt .

RUN apt-get update && apt-get install -y curl && pip install -r requirements.txt 


FROM build

WORKDIR /opt/etl
ENTRYPOINT [ "/bin/bash", "-c",  "./elasticsearch/init_indices.sh && celery -A etl worker -l info -B" ]

COPY . .
RUN chmod +x ./elasticsearch/init_indices.sh
