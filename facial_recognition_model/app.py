import os
import time
from PIL import Image
from werkzeug.utils import secure_filename
from scipy.io.wavfile import write
import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
#import pyaudio
import io
import struct
import requests
import re
from flask import Flask, jsonify, request
from io import BytesIO
import base64
import json
from flask import json
from flask import Flask, render_template,request
from flask import Flask, request, redirect, url_for
from urllib3.contrib.appengine import AppEngineManager
import certifi
from base64 import decodestring
import numpy as np
#from keras.preprocessing import image 
from skimage.transform import resize
#from keras.models import load_model
from tensorflow import keras
from imutils import face_utils
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from azure.storage.blob import BlockBlobService 
from azure.storage.blob import ContentSettings
import pyodbc
import cv2
import argparse
import imutils
import dlib
import urllib3
app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    return render_template('camera1.html')
@app.route('/predict', methods=['GET', 'POST'])
def upload():
    tok=request.get_json()
    token=tok['img']
    import base64
    head,tail = token.split(';')
    _,enc = head.split(':') # TODO: check if the beginning is "charset"
    _,msg = tail.split(',') # TODO: check that the beginning is "base64"
    import text_to_image
    #image = msg.encode('utf-8')
    #encoded_image_path = text_to_image.encode(msg, "imae.png")
    with open('images/NewPicture.jpg', 'wb') as file_to_save:
        file_to_save.write(base64.b64decode(msg))
        print('yesss done')
        #im = Image.open(io.BytesIO(image))
    def face(img, classifier, scaleFactor, minNeighbors, color, text):
        # Converting image to gray-scale
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # detecting features in gray-scale image, returns coordinates, width and height of features
        features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
        coords = []
        # drawing rectangle around the feature and labeling it
        for (x, y, w, h) in features:
            cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
            cv2.putText(img, text, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
            coords = [x, y, w, h]
        return coords,img
    # Method to detect the features
    def detect(img, faceCascade):
        color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0)}
        coords,img = face(img, faceCascade, 1.1, 10, color['blue'], "Face")
        # If feature is detected, the face method will return the x,y coordinates and width and height of rectangle else the length of coords will be 0
        if len(coords)==4:
            # Updating region of interest by cropping image
            img = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]
            # Passing roi, classifier, scaling factor, Minimum neighbours, color, label text
        return img
    # Loading classifiers
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # Capturing real time video stream. 0 for built-in web-cams, 0 or -1 for external web-cams
    img = cv2.imread("images/NewPicture.jpg")
    img = detect(img, faceCascade)
    # Writing processed image in a new window
    cv2.imwrite('images/NewPicture.jpg',img)
    cv2.destroyAllWindows()
    block_blob_service = BlockBlobService(account_name='xray', account_key='q1r80GTvqFb4qIwnBGeZ4oGmc36XHV/ATmbmuJtY1TkKW9timUCsDE2m9WL4X/J0L26qK2Mo9H3IF7/i/UnjlA==')
    #print("Image" ,img)
    block_blob_service.create_blob_from_path(
        'xrayimage',
        'firstblood.jpg',
        'images/NewPicture.jpg',
        content_settings=ContentSettings(content_type='image/jpeg'))
    server = 'virutal.database.windows.net'
    database = 'COVID19-db'
    username = 'Ismiledb'
    password = 'Ismile@123'
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    cursor.execute("Insert into Images (Img) Select BulkColumn FROM OPENROWSET( BULK 'firstblood.jpg', DATA_SOURCE = 'ImageSource1', SINGLE_BLOB) AS ImageFile;")
    cnxn.commit()
    text="File uploaded successfully"
    print()
    print(text)
    return ''
@app.route('/result',methods=['GET','POST'])
def result():
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    # load the input image, resize it, and convert it to grayscale
    image = cv2.imread("images/NewPicture.jpg")
    image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale image
    rects = detector(gray, 1)
    c=1
    # loop over the face detections
    for (i, rect) in enumerate(rects):
        # determine the facial landmarks for the face region, then
        # convert the landmark (x, y)-coordinates to a NumPy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        # loop over the face parts individually
        for (name, (i, j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
            # clone the original image so we can draw on it, then
            # display the name of the face part on the image
            clone = image.copy()
            cv2.putText(clone, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 0, 255), 2)
            # loop over the subset of facial landmarks, drawing the
            # specific face part
            for (x, y) in shape[i:j]:
                cv2.circle(clone, (x, y), 1, (0, 0, 255), -1)
            # extract the ROI of the face region as a separate image
            (x, y, w, h) = cv2.boundingRect(np.array([shape[i:j]]))
            roi = image[y-15:y + h+15, x-15:x + w+15]
            roi = imutils.resize(roi, width=250, inter=cv2.INTER_CUBIC)
            print(x, y, w, h)
            # show the particular face part
            #cv2.imshow("ROI", roi)
            #cv2.imshow("Image", clone)
            #cv2.waitKey(0)
            cv2.imwrite("images/Img"+str(i)+".jpg",roi)
        # visualize all facial landmarks with a transparent overlay
        #output = face_utils.visualize_facial_landmarks(image, shape)
        #cv2.imshow("Image", output)
        #cv2.waitKey(0)
    print("--------------------------------")
    fat=[]
    #items = os.listdir('C:/iSmile TEch/Drowsiness Detection/diFatigue-dataset.tar/data')
    #items = os.litdir('/content/data')
    items= ['Img36.jpg','Img42.jpg','Img48.jpg']
     #print(items)
    mapper={
        1:"Fatigue",
        0:"Non-Fatigue"
    }
    s=''
    for item in items:
        im = Image.open('images/'+item).convert('LA')
        im = im.resize((64,32),Image.ANTIALIAS)
        pix_val = list(im.getdata())  
        pix_val_flat = [sets[0] for sets in pix_val]
        s += ' '.join(str(x) for x in pix_val_flat)
        if(item == 'Img48.jpg'):
            break
        s += ' '
    fat.append(s)
    #print(len(fat[0].split(' ')))
    MODEL_PATH = r'model_f.h5'
    model =  keras.models.load_model(MODEL_PATH)
    temp = np.array(fat[0].split(' ')).reshape(64,32,3).astype('float32')
    #img_arr_f = np.stack(img_arr,axis=0)
    # print(temp.shape)
    temp = temp / 255
    # print(temp)
    print(mapper[model.predict_classes(temp.reshape(1,64,32,3))[0]])
    result=mapper[model.predict_classes(temp.reshape(1,64,32,3))[0]]
    print(result)
    return render_template('thank.html',result=result)
if __name__ == "__main__":
    app.run(debug=False)