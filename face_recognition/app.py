from flask import Flask
from PIL import Image
import requests
from io import BytesIO

import face_recognition

app = Flask(__name__)

def get_face_encoding( image_url ):
    response = requests.get(image_url)
    image = face_recognition.load_image_file(BytesIO(response.content))

    return face_recognition.face_encodings(image)[0]

# people = [[name, face_encoding], ...]
def get_people_on_image( image_url, people ):
    response = requests.get(image_url)
    image = face_recognition.load_image_file(BytesIO(response.content))

    face_encodings = face_recognition.face_encodings(image)
    face_locations = face_recognition.face_locations(image)

    result = []


    for i in range(len(face_encodings)):
        for person in people:
            if face_recognition.compare_faces([face_encodings[i]], person[1])[0]:
                result.append([person[0], face_locations[i]])
                break

    return result


@app.route('/')
def hello_world():
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/President_Barack_Obama.jpg/192px-President_Barack_Obama.jpg";

    image_url2 = "https://upload.wikimedia.org/wikipedia/commons/0/0e/Donald_Trump_Pentagon_2017.jpg"
    image_url3 = "https://cdn.cnn.com/cnnnext/dam/assets/170305143551-trump-obama-split-exlarge-169.jpg"
    people = [["Obama", get_face_encoding(image_url)],
        ["Trump", get_face_encoding(image_url2)]]

    return get_people_on_image(image_url3, people)



    return "hello";
