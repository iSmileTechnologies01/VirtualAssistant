from flask import Flask, render_template, request, redirect
import requests
import json
app = Flask(__name__)
CHECK = 0
@app.route("/")
def home():
    if(CHECK == 0):
        return render_template("wifi.html")
    URL = "http://localhost:3000/check"
    try:
        uResponse = requests.get(URL)
    except requests.ConnectionError:
       return "Connection Error"

    response = json.loads(uResponse.text)
    if(response['status'] == 'Yes'):
        return redirect("http://finalmodel.azurewebsites.net", code=302)
    else:
        return render_template("wifi.html")


@app.route('/form')
def form():
    URL = "http://localhost:3000/search"
    try:
        uResponse = requests.get(URL)
    except requests.ConnectionError:
       return "Connection Error"  
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    choices = []
    for element in data:
        choices.append(element['ssid'])
    print(choices)
    return render_template('form.html',choices=choices)

@app.route('/data/', methods = ['POST','GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        password = ''
        wifi = ''
        for key,value in form_data.items():
            if(key =='choice'):
                wifi += value
            if(key == 'Password'):
                password += value
        dictToSend = {'Password':password}
        print(dictToSend)
        URL = "http://localhost:3000/connect/" + wifi
        print(URL)
        res = requests.post(URL, json=dictToSend)
        print ('response from server:',res.text)
        dic = json.loads(res.text)
        print('return status:', dic['status'])
        
        return render_template('data.html',form = form_data, resText=dic['message'], status=dic['status'])