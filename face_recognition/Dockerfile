FROM ubuntu:18.10

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip cmake

RUN pip3 install face_recognition
RUN pip3 install flask

ENV FLASK_APP app.py
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

COPY . /app
WORKDIR /app

CMD flask run