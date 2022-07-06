FROM python:3.10-slim AS build

COPY requirements.txt ./

RUN apt-get update && apt-get install -y curl build-essential python-dev \
     && pip install --upgrade pip \
     && pip install -r requirements.txt


FROM python:3.10-slim

WORKDIR /opt/app
EXPOSE 8000
ENTRYPOINT ["uwsgi", "--strict", "--ini", "uwsgi.ini"]

COPY --from=build /usr/local /usr/local
RUN  mkdir -p /var/www/static/

COPY . .
