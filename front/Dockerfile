FROM python:3-alpine

COPY . /images_mongodb
WORKDIR /images_mongodb

RUN pip3 install -r requirements.txt

CMD python -u app.py
