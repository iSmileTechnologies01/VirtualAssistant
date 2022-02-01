

from flask import Flask, render_template,request,jsonify
import requests
import geocoder
import urllib.parse
app = Flask(__name__)
'''

'''

@app.route("/")
def index():
	#Import Libraries
	return render_template('index.html')

@app.route("/thankyou", methods=['POST'])
def thank_you():
	# Then get the data from the form
	address = str(request.form['loc'])
	print(address)
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
	return render_template('thankyou.html',result=hopitals_add)

result=[]
@app.route("/user_loc", methods=['POST'])
def user_loc():

	data = request.get_json()
	#print("data {}".format(data))
	URL = "https://discover.search.hereapi.com/v1/discover"
	latitude =  str(data[0])
	longitude = str(data[1])
	print(latitude,latitude)
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
	global result
	result.clear()
	for i in range(5):
		address =  data['items'][i]['address']['label']
		result.append(address)
	
	return '0'


@app.route("/resultPage")
def resultPage():

	#print('in resultPage {}'.format(result))
	return render_template('thankyou.html',result=result)




if __name__ == '__main__':
    app.run(debug=True)


