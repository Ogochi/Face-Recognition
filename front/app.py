from flask import Flask, redirect, url_for, request,render_template
import pymysql.cursors
from pymongo import MongoClient
import pika
import time
import ast
import base64

app = Flask(__name__)


def setup_mysql():
	try:
		global mysql_conn
		mysql_conn = pymysql.connect(host='mysql',user='michal',password='pass',db='images_db')
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
	_images = db.images.find()
	images = [image for image in _images]
	_encodings = db.encodings.find()
	encodings = [encoding for encoding in _encodings]
	_people = db.people.find()
	people = [hum for hum in _people]

	setup_mysql()
	with mysql_conn.cursor() as cursor:
		cursor.execute("SELECT * FROM images")
		results = cursor.fetchall()
		cursor.close()
		mysql_conn.close()

		return render_template('images.html', results=results, toList=ast.literal_eval)

@app.route('/people')
def people():
	_images = db.images.find()
	images = [image for image in _images]
	_encodings = db.encodings.find()
	encodings = [encoding for encoding in _encodings]
	_people = db.people.find()
	people = [hum for hum in _people]
	return render_template('people.html',images=images,encodings=encodings,people=people)


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

	return images()


@app.route('/add_image', methods=['POST'])
def add_image():
	channel.basic_publish(exchange='',
		routing_key='face_recognition',
		body='add_image;{}'.format(request.form['image_url']))

	return images()

def encodeStr(s):
	 return "-".join([str(ord(c)) for c in s])

@app.route('/image/<int:img_id>')
def show_image(img_id):
		setup_mysql()
		with mysql_conn.cursor() as cursor:
			cursor.execute("SELECT * FROM images WHERE {} = id".format(img_id))
			results = cursor.fetchall()
			cursor.close()
			mysql_conn.close()

			return render_template('img.html',image=results[0], people=ast.literal_eval(results[0][2]), encode=encodeStr)

if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)
