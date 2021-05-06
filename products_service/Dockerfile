
FROM python:3.9

RUN mkdir products_service

COPY products products_service/products
COPY products_service products_service/products_service
COPY requirements.txt products_service/requirements.txt
COPY db.sqlite3 products_service/db.sqlite3
COPY manage.py products_service/manage.py

RUN apt-get update && apt-get upgrade -y && \
    apt-get install nano && \
    apt-get install bash && \
    pip install -r products_service/requirements.txt

WORKDIR /products_service/
