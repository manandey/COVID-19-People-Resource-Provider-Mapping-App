from pymongo import MongoClient
from math import radians, cos, sin, asin, sqrt
from random import seed
from random import randint
import datetime

class NGOMatch:
    def __init__(self, lat, lon, cap):
        self.lat = lat
        self.lon = lon
        self.topNGOs = []
        # heapify( self.h)
     

    # def match():
    
    def compareNGOInfo(self):
        client = MongoClient(port = 27017)
        db = client.DaanMatch
        for doc in db.ngo_details.find({"Mobile": {"$ne" : ""}}):
            name = doc['Ngo Name']
            mobile = doc['Mobile']
            lat = doc['Latitude']
            lon = doc['Longitude']

            sat_r = doc['Satisfaction_rating']
            resp_r = doc['Response_rating']
            n_rat = doc['Number_ratings']
            last_active = doc['Last_active']

            print(self.calcScore(53.31861111111111, -1.6997222222222223, -2, 3, 40, datetime.date(2018,4,20)))
            break 

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

        print(dist, rating, last_act_score)
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
        
        # Radius of earth in kilometers. Use 3956 for miles 
        r = 6371
        
        # calculate the result 
        return(c * r) 
o = NGOMatch(53.32055555555556, -1.7297222222222221, 5)
o.compareNGOInfo()
