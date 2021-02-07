from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
import tensorflow as tf
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

#from tensorflow.keras.applications.resnet50 import ResNet50
#model = ResNet50(weights='imagenet')
#model.save('./resnet.h5')
# print('Model loaded. Check http://127.0.0.1:5000/')

#reload_model = tf.keras.models.load_model('./keras_model.h5')
#reload_model.summary()

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
#MODEL_PATH = './food3fin3.h5' #三個
MODEL_PATH = './food3fin5.h5'
# Load your trained model
model = tf.keras.models.load_model(MODEL_PATH)
#model._make_predict_function()          # Necessary
# print('Model loaded. Start serving...')

print('Model loaded. Check http://127.0.0.1:5000/')

## 辨別食物類別(FOOD-11)
classification=["Bread", "Supplement","Fruit","Noodles"]
import matplotlib.pyplot as plt
from skimage.transform import resize

#辨識類別
#def model_predict(img_path, model):
    #img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    #x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    #x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    #x = preprocess_input(x, mode='caffe')

   # preds = model.predict(x)
   # return preds

## 辨識食物
def recognize_food(img_path,model): 
    new_image=plt.imread(img_path)
    #img=plt.imshow(new_image)
    resized_image=resize(new_image, (224,224,3)) #resize the image
    #img = plt.imshow(resized_image)
    # get the models predictions
    predictions = model.predict(np.array([resized_image]))
    # sort the predictions from least to greatest
    list_index=[0,1,2,3]
    x=predictions
    for i in range(4):
        for j in range(4):
            if x[0][list_index[i]] > x[0][list_index[j]]:
                temp= list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    #print the first 5 prediction
    for i in range(2):
        foods=classification[list_index[0]]
        #print(classification[list_index[i]],':', predictions[0][list_index[i]]*100,'%')
    
    
    return foods

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('reconize(camera).html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        #preds = model_predict(file_path, model)
        preds=recognize_food(file_path,model)

        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            # Simple argmax
        #pred_class = decode_predictions(preds, top=1)   # ImageNet Decode
        #result = str(pred_class[0][0][1])               # Convert to string
        result = str(preds) 
        #result=preds
        return result
    return None

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True, use_reloader=False)
   
    #app.run(host='127.0.0.1', port=8000)

    