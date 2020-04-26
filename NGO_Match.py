from pymongo import MongoClient
from math import radians, cos, sin, asin, sqrt
from random import seed
from random import randint
import datetime
import heapq
from itertools import count

class NGOMatch:
	def __init__(self, lat, lon):
		self.lat = lat
		self.lon = lon
		# heapify( self.h)
	
	def compareNGOInfo(self):

		topNGOs = []
		cap=7
		cnt = count()
		heapq.heapify(topNGOs)
		client = MongoClient(port = 27017)
		db = client.DaanMatch

		for doc in db.ngoDetails.find({"Mobile": {"$ne" : ""}}):
			try:
				name = doc['Ngo Name']
				mobile = doc['Mobile']
				lat = float(doc['latitude'])
				lon = float(doc['longitude'])

				sat_r = int(doc['Satisfaction_rating'])
				resp_r = int(doc['Response_rating'])
				n_rat = int(doc['Number_ratings'])
				last_active = doc['Last_active'].split('-')

				year = int(last_active[2])
				month = int(last_active[1])
				day = int(last_active[0])

				#calculate score for the NGO
				score = self.calcScore(lat, lon, sat_r, resp_r, n_rat, datetime.date(year,month,day))

				if len(topNGOs)<cap:
					heapq.heappush(topNGOs, (score, next(cnt), {'Name': name, 'Mobile': mobile}))
				else:
					top = heapq.nsmallest(1, topNGOs)
					
					if top[0][0]<score:
						top = heapq.heappop(topNGOs)
						heapq.heappush(topNGOs, (score, next(cnt), {'Name': name, 'Mobile': mobile}))
					
			except:
				continue
		return topNGOs
			

	def calcScore(self, nlat, nlon, resp_r, sat_r, n_rat, last_active):

		#distance_score
		dist = self.calcDist(nlat, self.lat, nlon, self.lon)
	
		dist_score = int(1-(dist/5))             # Taking max preferred dist to be 5 km

		#rating score
		rating = (0.4*resp_r+0.6*sat_r)*n_rat

		#last_active score
		seed(1)
		today = datetime.datetime.date(datetime.datetime.now())
		last_act_score = (abs(today-last_active).days/30)*randint(0,10)
        
        #total score
		score = 0.5*dist_score + 0.3*rating - 0.2*last_act_score
		
		return score
	
	def calcDist(self, lat1, lat2, lon1, lon2):
		lon1 = radians(lon1) 
		lon2 = radians(lon2) 
		lat1 = radians(lat1) 
		lat2 = radians(lat2)
	
		# Haversine formula  
		dlon = lon2 - lon1  
		dlat = lat2 - lat1 
		a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
		c = 2 * asin(sqrt(a))  
		r = 6371
		return(c * r) 
