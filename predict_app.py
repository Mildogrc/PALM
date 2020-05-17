import base64
import numpy as np
import io
import cv2
from PIL import Image
from PIL import ImageStat
import keras
from keras import backend as K
from keras.models import load_model
from flask import request
from flask import jsonify
from flask import Flask
from flask import render_template
from flask import redirect
import tensorflow as tf
from keras.models import Sequential, Model
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.preprocessing.image import ImageDataGenerator,load_img, img_to_array
from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Input, Flatten, SeparableConv2D
from keras.layers import GlobalMaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.layers.merge import Concatenate
from keras.models import Model
from keras.optimizers import Adam, SGD, RMSprop
from keras.callbacks import ModelCheckpoint, Callback, EarlyStopping
from keras.utils import to_categorical
import math
import random
import string
import datetime
import time

app = Flask(__name__)

def get_model():
    global model,graph
    model = create_model()
    model.summary()
    model.load_weights('./PALM_MODEL.h5')
    graph = tf.get_default_graph()
    print(" * Model loaded!")

def preprocess_image(img):
    img = cv2.imread(str("temp.jpg"))
    img = cv2.resize(img, (224,224))
    if img.shape[2] ==1:
        img = np.dstack([img, img, img])
    else:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32)/255.

    img = np.expand_dims(img, axis = 0)

    return img

def create_model():
    input_image = Input(shape = (224, 224, 3), name = 'img_input')
    x = Conv2D(64, (3, 3), activation = 'relu', padding = 'same', name = 'conv2D1_1')(input_image)
    x = Conv2D(64, (3, 3), activation = 'relu', padding = 'same', name = 'conv2D1_2')(x)
    x = MaxPooling2D((2, 2), name = 'max_pool_1')(x)

    x = SeparableConv2D(128, (3, 3), activation = 'relu', padding = 'same', name = 'conv2D2_1')(x)
    x = BatchNormalization(name = 'bn1')(x)
    x = SeparableConv2D(128, (3, 3), activation = 'relu', padding = 'same', name = 'conv2D2_2')(x)
    x = MaxPooling2D((2, 2), name = 'max_pool_2')(x)

    x = SeparableConv2D(256, (3, 3), activation = 'relu', padding = 'same', name = 'conv2D3_1')(x)
    x = BatchNormalization(name = 'bn2')(x)
    x = SeparableConv2D(256, (3, 3), activation = 'relu', padding = 'same', name = 'conv2D3_2')(x)
    x = MaxPooling2D((2, 2), name = 'max_pool_3')(x)

    x = Flatten(name = 'flatten')(x)
    x = Dense(256, activation = 'relu', name = 'fc1')(x)
    x = Dropout(0.5, name = 'do1')(x)
    x = Dense(128, activation = 'relu', name = 'fc2')(x)

    x = Dense(2, activation = 'softmax', name = 'fc4')(x)

    model = Model(inputs = input_image, outputs = x)

    return model

def inv_log_transformation(value):
    Base = 10**(1.1)
    value = 1/value
    prob = math.log(value,Base)
    prob = 10*prob
    if prob <=0:
        prob = 0
    elif prob <= 40:
        prob = prob/4
    elif prob <= 60:
        prob = 4*prob - 150
    elif prob < 100:
        prob = prob/4 +75
    else:
        prob = 100
    prob = round(prob,2)
    prob = "{:.2f}".format(prob)


    return prob

   


print("loading keras model...")
get_model()
def randomString(stringLength=10):
    letters = string.ascii_lowercase
    strT = ''.join(random.choice(letters) for i in range(stringLength))
    return "static/StoredImages/" + strT

#it will launch here: "http://0.0.0.0:5000/static/predict2.html"
@app.route("/predict", methods=['POST'])
def predict():
    message = request.get_json(force=True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    f = open("temp.jpg","w+")
    f.write(decoded)
    print(is_grayscale("temp.jpg"))
    currentDT = datetime.datetime.now()
    currentDT = str(currentDT).split(' ')[1].replace('.',',')
    filepath = randomString(8) + currentDT + ".jpg"
    print(filepath)
    f = open(filepath,"w+")
    f.write(decoded)
    f.close()
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image)
    with graph.as_default():
        prediction = model.predict(processed_image).tolist()
    
    prob = inv_log_transformation(prediction[0][0])
    print(prob)

    response = {
        'prediction': {
            'prob' : prob,
            'filepath' : filepath
        }
    }
    time.sleep(5)
    return jsonify(response)

@app.route('/hello',methods=['POST'])
def hello():
    message = request.get_json(force=True)
    print("milu is the best")
    print(message)
    name = message['name']
    response = {'greeting': 'Hello,' + name + '!'}
    return jsonify(response)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/')
@app.route('/static/<path:yourmom>')
def rickrollhackers(yourmom):
    print(yourmom)
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')




