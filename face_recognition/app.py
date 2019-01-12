from PIL import Image
import requests
from io import BytesIO
from pymongo import MongoClient

import pika
import face_recognition

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
            if face_recognition.compare_faces([face_encodings[i]], person["face_encoding"])[0]:
                result.append([person["person_name"], face_locations[i]])
                break

    return result

#MONGODB
client = MongoClient("jnp3_mongo",27017)
db = client.images

def handle_message(ch, method, properties, body):
    body = body.split(':')

    if body[0] == 'add_person':
        # event:img_url:person_name
        face_encoding = get_face_encoding(body[1])
        db.encodings.insert_one({
            "face_encoding": face_encoding,
            "person_name": body[2]
        })

    elif body[0] == 'add_image':
        # event:image_url
        people_on_image = get_people_on_image(body[1], db.encodings.find())
        db.images.insert_one({
            "image_url": body[1],
            "people": people_on_image
        })


# RABBITMQ
credentials = pika.PlainCredentials('user', '2137')
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit',
    5672, '/', credentials))
channel = connection.channel()
channel.queue_declare(queue='face_recognition')

channel.basic_consume(handle_message, queue='face_recognition', no_ack=True)
channel.start_consuming()
