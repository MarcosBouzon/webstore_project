
FROM python:3.9

RUN mkdir webstore_service

COPY frontend webstore_service/frontend
COPY webstore webstore_service/webstore
COPY requirements.txt webstore_service/requirements.txt
COPY db.sqlite3 webstore_service/db.sqlite3
COPY manage.py webstore_service/manage.py

RUN apt-get update && apt-get upgrade -y && \
    apt-get install nano && \
    apt-get install bash && \
    pip install -r webstore_service/requirements.txt

WORKDIR /webstore_service/

