from flask import Flask, redirect, url_for, request,render_template
from pymongo import MongoClient
import pika

app = Flask(__name__)

# MONGODB
client = MongoClient("jnp3_mongo",27017)
db = client.images

# RABBITMQ
credentials = pika.PlainCredentials('user', '2137')
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit',
    5672, '/', credentials))
channel = connection.channel()
channel.queue_declare(queue='face_recognition')

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

@app.route('/add_person', methods=['POST'])
def add_person():
	person_doc = {
		'image_url':request.form['image_url'],
		'person_name': request.form['person_name']
	}
	db.people.insert_one(person_doc)

	message_body = 'add_person:{}:{}'.format(person_doc['image_url'], person_doc['person_name'])
	channel.basic_publish(exchange='',
		routing_key='image',
		body=message_body)

	return redirect(url_for('images'))

@app.route('/add_image', methods=['POST'])
def add_image():
	channel.basic_publish(exchange='',
		routing_key='image',
		body='add_image:{}'.format(request.form['image_url']))

	return redirect(url_for('images'))

if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)
