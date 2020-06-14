#!/usr/bin/env python3
import connexion
import redis
import tensorflow as tf
from werkzeug.utils import secure_filename
from keras.preprocessing import image
import numpy as np
import datetime
import json
from flask_cors import CORS

# Fetch all out results out of the "DB" and return them as is.
def inference_get():
    try:
        queue = db.lrange('all_inferences', 0, -1)
        output = []
        for q in queue:
            output.append(json.loads(q.decode('utf-8')))

        return output
    except Exception as e:
        return 'Internal server error: '+ str(e), 500

# Get the file, inference, store the results in Redis and send them back as JSON
def inference_post(body):
    try:
        uploaded_file = connexion.request.files['file_name']
        filename = secure_filename(uploaded_file.filename)
        img_path = "/tmp/uploads/{}{}".format(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"),filename) # Make the filename unique for duplicates.

        # If we don't want to save the image we should be able to read this as a Buffered Byte IO stream.
        uploaded_file.save(img_path)
        img = image.load_img(path=img_path,target_size=(28,28), color_mode='grayscale')

        img = preprocess_img(img)

        predictions = model.predict(img)
        index = int(predictions.argmax())
        confidence = float(predictions[0][index])
        output = {'confidence': confidence, 'prediction':index, 'img_url':img_path[4:]}

        # We are using redis as a form of inmemory DB, not it's ideal purpose but it works.
        db.rpush('all_inferences', json.dumps(output))

        return output
    except Exception as e:
        return 'Internal server error: '+ str(e), 500

def preprocess_img(img):
    img = image.img_to_array(img)
    img = img.reshape((1,28,28,1))
    img = img / 255.0
    return img

app = connexion.App(__name__, specification_dir='./openapi/')
db = redis.StrictRedis(host='localhost', port=6379, db=0) # Ideally we have a different redis pod, but for simplicity lets just self host.
CORS(app.app) 
model = tf.keras.models.load_model('./numberClassifier.h5')

app.add_api('openapi.yaml',
            arguments={'title': 'Number Classifier API'},
            pythonic_params=True)

# set this up to be callable by uWSGI
application = app.app
