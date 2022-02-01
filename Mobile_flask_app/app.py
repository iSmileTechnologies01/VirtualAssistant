from glob import glob
import os
import numpy as np
import pandas as pd
import random
from skimage.io import imread
import matplotlib.pyplot as plt
import tensorflow
import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img

from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from azure.storage.blob import BlockBlobService 
from azure.storage.blob import ContentSettings
import pyodbc

MODEL_PATH = 'xray_model.h5'
model = load_model(MODEL_PATH)

app = Flask(__name__)
pass_id=0

@app.route("/")
def passcode():
    #Import Libraries
    return render_template('ask_passcode.html')

@app.route('/upload_Image')
def index():
    global pass_id
    pass_id = request.args.get('last')
    return render_template('Xupload.html')

    
def upload_model(file_path):
    normal_or_pneumonia = ['NORMAL', 'PNEUMONIA']
    img_choice = (file_path)
    img = load_img(img_choice, target_size=(150, 150))
    img = img_to_array(img)
    plt.imshow(img / 255.)
    x = preprocess_input(np.expand_dims(img.copy(), axis=0))
    pred_class = model.predict_classes(x)
    pred = model.predict(x)
    lst=[]
    lst.append(pred_class[0])
    if pred_class[0] == 0:
        lst.append(pred[0][0].round(1))
    else:
        lst.append(pred[0][1].round(1))   	
    return lst
    
@app.route('/predict', methods=['GET', 'POST'])
def upload():
    pid = 1
    img = request.files['inpFile']
    basepath = os.path.dirname(__file__)
    file_path = os.path.join(basepath, 'uploads', secure_filename(img.filename))
    img.save(file_path)
    ##calling upload_model function
    X_ray_value = upload_model(file_path)
    #img.save(file_path)
    predicted_class = X_ray_value[0]
    predicted_value = X_ray_value[1]

    block_blob_service = BlockBlobService(account_name='xray', account_key='q1r80GTvqFb4qIwnBGeZ4oGmc36XHV/ATmbmuJtY1TkKW9timUCsDE2m9WL4X/J0L26qK2Mo9H3IF7/i/UnjlA==')
    #print("Image" ,img)
    block_blob_service.create_blob_from_path(
        'xrayimage',
        'firstblood.jpg',
        'uploads/'+img.filename,
        content_settings=ContentSettings(content_type='image/jpeg'))

    server = 'virutal.database.windows.net'
    database = 'COVID19-db'
    username = 'Ismiledb'
    password = 'Ismile@123'
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    #cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    personid=pass_id
    query="INSERT INTO XrayDetails(Personid,Prdicted_value,Prdicted_Class) VALUES(?,?,?)"
    v1 = (str(personid),str(predicted_value), str(predicted_class))
    cursor.execute(query,v1)
    cnxn.commit()
    #cursor.execute("Insert into XrayDetails (Xrayimage) Select BulkColumn FROM OPENROWSET( BULK 'firstblood.jpg', DATA_SOURCE = 'ImageSource1', SINGLE_BLOB) AS ImageFile;")
    cursor.execute("UPDATE XrayDetails SET Xrayimage = (Select BulkColumn FROM OPENROWSET( BULK 'firstblood.jpg', DATA_SOURCE = 'ImageSource1', SINGLE_BLOB) AS ImageFile )WHERE Personid = {} ;".format(personid))
    cnxn.commit()
    text="File uploaded successfully"
    #print(text)
    os.remove(file_path)
    return text

@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('X_result.html')

if __name__ == "__main__":
    app.run(debug=True)
