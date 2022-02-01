import base64
from gtts import gTTS
import playsound
import pyaudio
import glob 
import random
import IPython.display as ipd
import librosa
from PIL import Image
from flask import json
from flask import Flask, render_template,request
from flask import Flask, request, redirect, url_for
from urllib3.contrib.appengine import AppEngineManager
import certifi
from base64 import decodestring
import pyodbc
import time
from scipy.io.wavfile import write
import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import io
import struct
import requests
import re
from flask import Flask, jsonify, request
from io import BytesIO
import json
import os
from skimage.transform import resize
from tensorflow import keras
from imutils import face_utils
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from azure.storage.blob import BlockBlobService 
from azure.storage.blob import ContentSettings
import pyodbc
import numpy as np
import argparse
import imutils
import dlib
import cv2
import urllib3
import requests
import geocoder
import urllib.parse

app = Flask(__name__)
res_voice=0
res_cough=0
result_facial=0
symp=''
danger=[]
result = []
passcde=0

@app.route('/')
def startit():
    return render_template('index1.html')
    
@app.route('/passcode')
def passcode():
    Fname = request.args.get('Fname')
    Lname = request.args.get('Lname')
    Age = request.args.get('Age')
    Country = request.args.get('Country')
    Zip_code = request.args.get('Zip_code')
    print("-------------------------")
    print(Fname)
    print(Lname)
    print(Age)
    print(Country)
    print(Zip_code)
    import pyodbc

    server = 'virutal.database.windows.net' 
    database = 'COVID19-db' 
    username = 'Ismiledb' 
    password = 'Ismile@123' 
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    cursor.execute("INSERT INTO PersonDetails(LastName,FirstName,Age,City) VALUES (?,?,?,?)",(Lname,Fname,Age,Country))
    cnxn.commit()

    cursor.execute("SELECT max(Personid) FROM PersonDetails WHERE LastName=? AND FirstName=? AND Age=? AND City=?",(Lname,Fname,Age,Country))
    row=cursor.fetchone()
    global passcde
    passcde=row[0]
    print(passcde)

    return render_template('passcode.html',passcde=passcde)

@app.route('/inner')
def inner():
    return render_template('inner.html')

@app.route("/survey")
def survey():
	global result
	global danger
	import pandas as pd
	import requests
	from bs4 import BeautifulSoup
	import csv

	url = 'https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/symptoms.html'
	page = requests.get(url)
	page.text
	soup = BeautifulSoup(page.text, 'html.parser')

	review_text_elem = soup.find_all('div',{'class':'col-md-12'})

	result=[li.string for li in review_text_elem[1].find('ul').findAll('li')]
	print()
	print()
	print(result)

	danger_elem = soup.find_all('div',{'class':'warning-signs-public'})

	danger=[li.string for li in danger_elem[0].find('ul').findAll('li')]
	print()
	print()
	print(danger)
	return render_template('Survey.html',result=result,danger=danger)

@app.route('/Survey_Result')
def thank_you_survey():

	print()
	print(passcde)
	print()
	final_res = []
	final_dan= []

	for i in result:
		final_res.append(request.args.get(i))
	print(final_res)	

	for i in danger:
		final_dan.append(request.args.get(i))
	print(final_dan)


	symptom=[]
	for i in range(len(result)):
		if final_res[i]=='yes':
			symptom.append(result[i])

	for i in range(len(danger)):
		if final_dan[i]=='yes':
			symptom.append(danger[i])

	mild=['Fever or chills', 'Cough', 'Fatigue','Muscle or body aches', 'Headache', 'Sore throat', 'Congestion or runny nose', 'New confusion']
	moderate=['Nausea or vomiting', 'Diarrhea']
	severe=['Shortness of breath or difficulty breathing','New loss of taste or smell', 'Trouble breathing', 'Persistent pain or pressure in the chest', 'Inability to wake or stay awake', 'Bluish lips or face']
	m=0
	mo=0
	s=0

	for i in symptom:
	  if i in mild:
	    m+=1
	  elif i in moderate:
	    mo+=1
	  elif i in severe:
	    s+=1 
	  else:
	    if i in result:
	    	mo+=1
	    	moderate.append(i)
	    else:
	    	s+=1
	    	severe.append(i)

	s_len=len(severe)
	mo_len=len(moderate)
	m_len=len(mild)
	temp=(s+m)/(s_len+m_len)

	print(m,mo,s,mo_len,s_len,m_len,temp)

	symp='Heya!'
	
	if m>4 and mo>0 and s>3:
		symp= "You seem to exhibit severe symptoms of COVID-19. There are 97% chances of threat. Please visit a clinical facility as soon as possible."
	elif m>4 and mo>0 and s>0:
		symp= "You seem to exhibit severe symptoms of COVID-19. There are 95% chances of threat. Please visit a clinical facility as soon as possible."
	elif m>4 and mo==0 and s>0:
		symp= "You seem to exhibit symptoms of of COVID-19. There are 90% chances of threat. Please visit a clinical facility as soon as possible."
	elif m>2 and mo>0 and s>0:
		symp= "You seem to exhibit symptoms of of COVID-19. There are 90% chances of threat. Please visit a clinical facility as soon as possible."
	elif s>3:
		symp= "You seem to exhibit symptoms of of COVID-19. There are 90% chances of threat. Please visit a clinical facility as soon as possible."
	elif m<4 and mo==0 and s>0:
		symp= "You seem to exhibit Mild symptoms of of COVID-19. There are 85% chances of threat. Please visit a clinical facility as soon as possible."
	elif m>2 and mo>0:
		symp= "You seem to exhibit considerable chances of COVID-19"
	elif m>3:
		symp= "You seem to exhibit considerable chances of COVID-19"
	elif m<=3 or mo>0:
		symp= "You seem to be safe. Stay Home Stay Safe!!"

	print("---------------------------------")
	Values=[]
	for i in range(len(symptom)):
		Values.append(symptom[i].split(" or")[0])
	print(Values)
	print("------------------------------------")

	import pyodbc

	server = 'virutal.database.windows.net' 
	database = 'COVID19-db' 
	username = 'Ismiledb' 
	password = 'Ismile@123' 
	cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor = cnxn.cursor()

	temp=[]
	quest=[]
	for i in range(len(Values)):
  		temp.append('SYMPTOM'+str(i+1))
  		quest.append('?')

	temp.append('ID')
	quest.append('?')

	x = ",".join(temp)
	y = ",".join(quest)

	SQLCommand = ("INSERT INTO SURVEY ("+x+") VALUES ("+y+");")
	cursor = cnxn.cursor()	
	Values.append(passcde)

	cursor.execute(SQLCommand,Values)
	cnxn.commit()

	return render_template('SurveyResult.html',symp = symp)

@app.route('/index', methods=['GET'])
def index():
	return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    tok=request.get_json()
    token=tok['reader']
    import base64
    head,tail = token.split(';')
    _,enc = head.split(':') # TODO: check if the beginning is "charset"
    _,msg = tail.split(',') # TODO: check that the beginning is "base64"
    #image = msg.encode('utf-8')
    #encoded_image_path = text_to_image.encode(msg, "imae.png")
    with open('NewPicture.wav', 'wb') as file_to_save:
        file_to_save.write(base64.b64decode(msg))
    return ''

@app.route('/result', methods=['GET', 'POST'])
def result():
    global res_voice
    global res_cough
    global symp
    #ipd.Audio('C:/Users/thiru/Downloads/vove/NewPicture.wav')
    data, sampling_rate = librosa.load('NewPicture.wav')
    n0 = 90000
    n1 = 90100
    y = data//1
    zeros = (y == 0).sum() 
    ones = (y == -1).sum()
    zero_crossings = librosa.zero_crossings(data[n0:n1], pad=False)
    print("zero_crossings are:" + str(sum(zero_crossings)))
    if (sum(zero_crossings) <=6 and zeros > ones):
        print('1')
        symp= 'you seem to have sore throat and Cough'

    elif(sum(zero_crossings) <= 6 and zeros < ones):
        res_voice=1
        res_cough=0
        symp= 'you seem to have sore throat but no Cough'

    elif(sum(zero_crossings) > 6 and zeros > ones):
        res_voice=0
        res_cough=1
        symp= 'your throat seems to be fine but you have Cough'
    else:
    	res_voice=0
    	res_cough=0
    	symp= "your throat seems to be fine and you don't have Cough"

    print("Result 1 is:",res_voice)
    print("Result 2 is :",res_cough)
    print("passcde is :",passcde)
    #a=passcde
    return render_template('camera1.html')

@app.route('/predict_facial', methods=['GET', 'POST'])
def uploaded():
    tok=request.get_json()
    token=tok['img']
    import base64
    head,tail = token.split(';')
    _,enc = head.split(':') # TODO: check if the beginning is "charset"
    _,msg = tail.split(',') # TODO: check that the beginning is "base64"
    #import text_to_image
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
@app.route('/result1',methods=['GET','POST'])
def result1():
    global result_facial
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
    res_facial=mapper[model.predict_classes(temp.reshape(1,64,32,3))[0]]
    print(res_facial)
    result_facial=int(model.predict_classes(temp.reshape(1,64,32,3))[0])
    print("Result Voice model is:",symp)
    print("Result facial is:",result_facial)
    print("Result 1 is:",res_voice)
    print("Result 2 is :",res_cough)
    print("passcde is :",passcde)
    server = 'virutal.database.windows.net'
    database = 'COVID19-db'
    username = 'Ismiledb'
    password = 'Ismile@123'
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    cursor.execute("UPDATE HealthResult SET Voice_result=?, Facial_model=?,cough_result=? WHERE Personid=?",(res_voice,result_facial,res_cough,passcde))
    cnxn.commit()
    return render_template('thank1.html',symp=symp,res_facial=res_facial)

@app.route('/barcode')
def barcode():
    passcode=passcde
    return render_template('barcode.html',passcode=passcode)

@app.route('/XrayResult')
def XrayResult():
    personid=passcde
    print(passcde)
    server = 'virutal.database.windows.net' 
    database = 'COVID19-db' 
    username = 'Ismiledb' 
    password = 'Ismile@123' 
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    #cursor.execute("SELECT TOP 1 * FROM dbo.XrayDetails where Personid=?,personid")
    query = "SELECT * FROM dbo.XrayDetails where Personid=?"
    cursor.execute(query,(personid,))
    row=cursor.fetchone()
    #print(row)
    print("--------------------------database connectivity-----------")
    #print("fetched data:"+str(row))
    pred_class=row[3]
    pred_value=row[2]
    #print(type(pred_value))
    #print(pred_class)
    text=""
    if pred_class == '0':
        text="Predicted class: Normal, Likelihood:"+str(pred_value) 
        if pred_value < '0.8':
            text+="with the WARNING of low confidence"            
    else:
        text="Predicted class: Pneumonia, Likelihood:"+str(pred_value)
        if pred_value < '0.8':
            text+="WARNING, low confidence" 

    print("text"+text)
    return render_template('xrayResult.html', result=text)

@app.route('/geo_location')
def geo_location():
	#Import Libraries
	return render_template('locator.html')

@app.route("/thankyou", methods=['POST'])
def thank_you():
	# Then get the data from the form
	address = str(request.form['loc'])
	#print(address)
	url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
	response = requests.get(url).json()
	URL = "https://discover.search.hereapi.com/v1/discover"
	latitude =  str(response[0]["lat"])
	longitude = str(response[0]["lon"])
	api_key = 'tu4m3GFeH7ze3oQDsOBqMpRk3-yFx7XyapfV92Yw-uo' # Acquire from developer.here.com
	query = 'hospitals'
	limit = 5
	PARAMS = {
				'apikey':api_key,
				'q':query,
				'limit': limit,
				'at':'{},{}'.format(latitude,longitude)
			} 

	# sending get request and saving the response as response object 
	r = requests.get(url = URL, params = PARAMS) 
	data = r.json()
	hopitals_add=[]
	for i in range(5):
		address =  data['items'][i]['address']['label']
		hopitals_add.append(address)

	#print(result)
	return render_template('thankyou.html',result_loc=hopitals_add)

result_loc=[]
@app.route("/user_loc", methods=['POST'])
def user_loc():

	data = request.get_json()
	#print("data {}".format(data))
	URL = "https://discover.search.hereapi.com/v1/discover"
	latitude =  str(data[0])
	longitude = str(data[1])
	#print(latitude,latitude)
	api_key = 'tu4m3GFeH7ze3oQDsOBqMpRk3-yFx7XyapfV92Yw-uo' # Acquire from developer.here.com
	query = 'hospitals'
	limit = 5
	PARAMS = {
				'apikey':api_key,
				'q':query,
				'limit': limit,
				'at':'{},{}'.format(latitude,longitude)
			} 

	# sending get request and saving the response as response object 
	r = requests.get(url = URL, params = PARAMS) 
	data = r.json()
	global result_loc
	result_loc.clear()
	for i in range(5):
		address =  data['items'][i]['address']['label']
		result_loc.append(address)
	
	return '0'


@app.route("/resultPage")
def resultPage():

	#print('in resultPage {}'.format(result_loc))
	return render_template('thankyou.html',result_loc=result_loc)


@app.route('/Rating')
def Rating():    
    print("rating url called")
    star = request.args.get('star')
    print("star {}".format(star))
    return "0"

if __name__ == "__main__":
    app.run(debug=True)