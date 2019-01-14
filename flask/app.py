from flask import Flask, redirect, url_for, request,render_template
from pymongo import MongoClient
import pika
import time

app = Flask(__name__)

def setup_mongo():
    try:
        client = MongoClient("jnp3_mongo",27017)
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
            5672, '/', credentials, heartbeat=0))
        global channel
        channel = connection.channel()
        channel.queue_declare(queue='face_recognition')
    except:
        time.sleep(2)
        setup_rabbit()

# RABBITMQ
setup_rabbit()

@app.route('/')
def images():
	print ("Wyswietlam!")
	_images = db.images.find()
	images = [image for image in _images]
	_encodings = db.encodings.find()
	encodings = [encoding for encoding in _encodings]
	_people = db.people.find()
	people = [hum for hum in _people]
	return render_template('images.html',images=images,encodings=encodings,people=people)

@app.route('/people')
def people():
	print ("Wyswietlam!")
	_images = db.images.find()
	images = [image for image in _images]
	_encodings = db.encodings.find()
	encodings = [encoding for encoding in _encodings]
	_people = db.people.find()
	people = [hum for hum in _people]
	return render_template('people.html',images=images,encodings=encodings,people=people)

@app.route('/old_view')
def old_view():
	print ("Wyswietlam!")
	_images = db.images.find()
	images = [image for image in _images]
	_encodings = db.encodings.find()
	encodings = [encoding for encoding in _encodings]
	_people = db.people.find()
	people = [hum for hum in _people]
	return render_template('old.html',images=images,encodings=encodings,people=people)


@app.route('/add_person', methods=['POST'])
def add_person():
	person_doc = {
		'image_url':request.form['image_url'],
		'person_name': request.form['person_name']
	}
	db.people.insert_one(person_doc)

	message_body = 'add_person;{};{}'.format(person_doc['image_url'], person_doc['person_name'])
	channel.basic_publish(exchange='',
		routing_key='face_recognition',
		body=message_body)

	print("Added person", flush=True)

	return images()


@app.route('/add_image', methods=['POST'])
def add_image():
	channel.basic_publish(exchange='',
		routing_key='face_recognition',
		body='add_image;{}'.format(request.form['image_url']))

	return images()

if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)
