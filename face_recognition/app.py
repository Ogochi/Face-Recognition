from PIL import Image
import requests
from io import BytesIO
from pymongo import MongoClient

import pymysql.cursors
import pika
import time
import face_recognition
import numpy as np


def setup_mysql():
	try:

		global mysql_conn
		mysql_conn = pymysql.connect(host='mysql',user='root',password='example',db='images_db')
	except:
		time.sleep(2)
		setup_mysql()

def setup_mongo():
    try:
        client = MongoClient("mongo",27017)
        global db
        db = client.images
    except:
        time.sleep(2)
        setup_mongo()

# MONGODB
setup_mongo()

def setup_rabbit():
    try:
        credentials = pika.PlainCredentials('user', '2137')
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit',
            5672, '/', credentials))
        global channel
        channel = connection.channel()
        channel.queue_declare(queue='face_recognition')
    except:
        time.sleep(2)
        setup_rabbit()

# RABBITMQ
setup_rabbit()


def get_face_encoding(image_url):
    response = requests.get(image_url)
    image = face_recognition.load_image_file(BytesIO(response.content))

    return face_recognition.face_encodings(image)[0]

# people = [[name, face_encoding], ...]
def get_people_on_image(image_url, people):
    response = requests.get(image_url)
    image = face_recognition.load_image_file(BytesIO(response.content))

    face_encodings = face_recognition.face_encodings(image)
    face_locations = face_recognition.face_locations(image)

    result = []
    for i in range(len(face_encodings)):
        for person in people:
            if face_recognition.compare_faces([face_encodings[i]], np.array(person["face_encoding"]))[0]:
                result.append([person["person_name"], face_locations[i]])
                break

    return result

def handle_message(ch, method, properties, body):
    try:
        body = "{}".format(body)[2:-1].split(';')

        if body[0] == 'add_person':
            # event:img_url:person_name
            face_encoding = get_face_encoding(body[1])
            db.encodings.insert_one({
                "face_encoding": face_encoding.tolist(),
                "person_name": body[2]
            })

        elif body[0] == 'add_image':
            # event:image_url
            people_on_image = get_people_on_image(body[1], db.encodings.find())
            db.images.insert_one({
                "image_url": body[1],
                "people": people_on_image
            })

            setup_mysql()
            with mysql_conn.cursor() as cursor:
                cursor.execute("INSERT INTO images (url,people) VALUES(\"{}\",\"{}\")".format(body[1], people_on_image))
            mysql_conn.commit()
            cursor.close()
            mysql_conn.close()

    except:
        print("Error during handling message!")

channel.basic_consume(handle_message, queue='face_recognition', no_ack=True)
print("waiting", flush=True)
channel.start_consuming()
print("ended")
