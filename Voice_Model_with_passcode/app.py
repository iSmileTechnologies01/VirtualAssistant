from flask import Flask, jsonify, request
from io import BytesIO
import base64
import re
import json
import datetime
from gtts import gTTS
import playsound
import pyaudio
import glob 
import os
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

app = Flask(__name__)
pass_id=0

@app.route("/")
def passcode():
	#Import Libraries
	return render_template('ask_passcode.html')

@app.route('/index', methods=['GET'])
def index():
	global pass_id
	pass_id = request.args.get('last')
	print()
	print(pass_id)
	print()
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
    fs = 44700 
    seconds = 6  
    #ipd.Audio('C:/Users/thiru/Downloads/vove/NewPicture.wav')
    data, sampling_rate = librosa.load('NewPicture.wav')
    n0 = 9000
    n1 = 9100
    y = data//1
    zeros = (y == 0).sum()
    ones = (y == -1).sum()
    zero_crossings = librosa.zero_crossings(data[n0:n1], pad=False)
    print(sum(zero_crossings))
    if (sum(zero_crossings) <= 10 and zeros > ones):
        result1=1
        result2=1
        symp= 'you seem to have sore throat and Cough'

    elif(sum(zero_crossings) <= 10 and zeros < ones):
        result1=1
        result2=0
        symp= 'you seem to have sore throat but no Cough'

    elif(sum(zero_crossings) > 10 and zeros > ones):
        result1=0
        result2=1
        symp= 'your throat seems to be fine but you have Cough'
    else:
    	result1=0
    	result2=0
    	symp= "your throat seems to be fine and you don't have Cough"

    print("Result 1 is:",result1)
    print("Result 2 is :",result2)
    print("pass_id is :",pass_id)
    #a=pass_id	
    server = 'virutal.database.windows.net'
    database = 'COVID19-db'
    username = 'Ismiledb'
    password = 'Ismile@123'
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    cursor.execute("UPDATE HealthResult SET Voice_result=?, Facial_model=? WHERE Personid=?",(result1,result2,pass_id))
    cnxn.commit()
      
    return render_template('thank.html',symp = symp)
if __name__ == "__main__":
    app.run(debug=False)