FROM python:3.10

WORKDIR /opt/etl
ENTRYPOINT [ "/bin/bash", "-c",  "./elasticsearch/init_indices.sh && python3 etl.py" ]

COPY requirements.txt ./

RUN pip install -r requirements.txt 

COPY . .
RUN chmod +x ./elasticsearch/init_indices.sh 
