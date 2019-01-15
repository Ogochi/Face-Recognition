FROM ubuntu:18.10

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip cmake

RUN pip3 install face_recognition
RUN pip3 install pika
RUN pip3 install requests
RUn pip3 install pymongo
RUN pip3 install PyMySQL

COPY . /app
WORKDIR /app

CMD python3 app.py
