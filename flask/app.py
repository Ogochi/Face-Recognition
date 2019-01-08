from flask import Flask, redirect, url_for, request,render_template
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("jnp3_mongo",27017)
db = client.images

@app.route('/')
def images():
	print ("Wyswietlam!")
	_images = db.images.find()
	images = [image for image in _images]

	return render_template('images.html', images=images)

@app.route('/dodaj', methods=['POST'])
def dodaj():
	image_doc = {
		'id':request.form['id'],
		'people': request.form['people']
	}
	db.images.insert_one(image_doc)
	return redirect(url_for('images'))

if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)
