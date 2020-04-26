from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from NGO_Match import NGOMatch 
import requests
from googletrans import Translator
from twilio.rest import Client
from pymongo import MongoClient
import datetime
app = Flask(__name__)

translator = Translator()
account_sid="ACf807961c8c8b19765668cfbda0c26fde"
auth_token = '24bf455d7cf1926ce0f7bf523ca60d7a'

@app.route("/sms", methods=['GET', 'POST'])

def receive_sms():
   
    
    from_number = request.form['From']
    to_number = request.form['To']
    body = request.form['Body']

    print(from_number, to_number, body)
    
    resp = MessagingResponse()
    
    message = ""
    translation=""

    if "FEEDBACK" in body.split()[0]:
    	body = body.split(':')[1]
    	body = body.split()
    	mob = body[0]
    	resp_rat = body[2]
    	sat_rat = body[4]
    	update_db(mob, resp_rat, sat_rat)
    else:
	    try:
		    print(body)
		    lat, lon = find_lat_lon(body)
		    nmatch = NGOMatch(lat, lon)
		    ngo = nmatch.compareNGOInfo()

		    print(lat, lon)

		    message = "Thank you for reaching out to us. Please try reaching out to the following NGOs for help.\n"
		    translation = str(translator.translate(message, dest = 'hi').text)
		    # print(translation)
		    translation+='\n'
		    for i in ngo:
		    	name = i[2]['Name']
		    	mob = i[2]['Mobile']
		    	# message = message.join(name)
		    	# message+='\n'
		    	message+=name+" "+mob+'\n'
		    	translation += name+" "+mob+'\n' 
		    send_sms(from_number)

	    except:
	    	message = "Sorry we couldn't find any NGOs near you" 
	    	translation = str(translator.translate(message, dest = 'hi').text)
    	
    message = message+"\n\n\n\n"+str(translation)
    resp.message(message)
    # print(message)
    return str(resp)

def find_lat_lon(location):

	URL = "https://maps.googleapis.com/maps/api/geocode/json"
	key = "AIzaSyCQI22Bkjzi_4VGOvsQcpUJuqWnGTnByV4"

	PARAMS = {'address': location, "key": key}
	r = requests.get(url=URL, params=PARAMS)

	data = r.json()

	latitude = data['results'][0]['geometry']['location']['lat']
	longitude = data['results'][0]['geometry']['location']['lng']

	return latitude, longitude


def send_sms(number):
	client = Client(account_sid, auth_token)
	# print("here")
	message = "Kindly write the NGO's phone number along with a rating from 1 to 5 on below criteria: \n\n Response Time:\n Satisfaction:\n\nExample:"
	translation = str(translator.translate(message, dest = 'hi').text)
	message+="\n\nFEEDBACK: 9334918561 R 4 S 5"
	translation+= "\n\nFEEDBACK: 9334918561 R 4 S 5"
	message = message+"\n\n\n\n"+str(translation)
	client.messages.create(
	                     body=message,
	                     # from_='+12056277965',
	                     from_='+18634501750',
	                     to=number
	                 )

def update_db(mob, res, sat):
	client = MongoClient(port = 27017)
	db = client.DaanMatch
	# for doc in db.ngoDetails.find({"Number_ratings": {"$ne" : "0"}}):
	# 	print(doc['Ngo Name'])
	today = datetime.datetime.date(datetime.datetime.now())
	date = str(today).split('-')
	today = date[2]+'-'+date[1]+'-'+date[0]
	for doc in db.ngoDetails.find({"Mobile": mob}):
		i, s, r, n = doc['_id'], int(doc['Satisfaction_rating']), int(doc['Response_rating']), int(doc['Number_ratings'])
		r=((r*n)+int(res))/(n+1)
		s=((s*n)+int(sat))/(n+1)
		print(r, s, n+1)
		db.ngoDetails.update_one({"_id":i},{"$set":{"Satisfaction_rating":s, "Response_rating":r, "Number_ratings":n+1, 'Last_active':today}})





if __name__ == "__main__":
    app.run(debug=True)