import re
# phrase="Hello my name is Peter and I'm 25 years old. I was born in 1991121. I have 1 child; he's a boy. That's about all"
regex= "\d{6}"
# match= re.findall(regex, phrase)
# print(match)

import pandas as pd
import requests

df = pd.read_excel ("C:\\Users\\I521271\\PycharmProjects\\NGO\\NGO.xlsx")
# df=df.head()
address=df['nr add']
# print(df.loc[116,'nr add'])
# print(len(address))
# print(address)
# for location in address:
#     print(location)
#     i=i.split(" ")
#     s = "+".join(i)
#     url="https://maps.googleapis.com/maps/api/geocode/json?address="+s+"&key=AIzaSyCQI22Bkjzi_4VGOvsQcpUJuqWnGTnByV4 "
#     print(url)

import requests
URL = "https://maps.googleapis.com/maps/api/geocode/json"
# location = "room Nargada Village, Danapur Cantt - Shivala Road, Patna, Bihar- 801503"
key = "AIzaSyCQI22Bkjzi_4VGOvsQcpUJuqWnGTnByV4"
datalist=[]
latitudelist=[]
longitudelist=[]
for location in address:
    PARAMS = {'address': location, "key": key}
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    latitude = data['results'][0]['geometry']['location']['lat']
    longitude = data['results'][0]['geometry']['location']['lng']
    datalist.append(data)
    latitudelist.append(latitude)
    longitudelist.append(longitude)
df["latitude"]=latitudelist
df["longitude"]=longitudelist
df["data"]=datalist
df.to_excel("New_NGO.xlsx")

# formatted_address = data['results'][0]['formatted_address']

# printing the output
# print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
# 	%(latitude, longitude,formatted_address))


# count1=0
# count3=0
# nozipcount=0
# yeszipcount=0
# for i in address:
#     print(i)
#     count1+=1
#     if(type(i)!=int):
#         count3 += 1
#         match=re.findall(regex,i)
#         if(match ==[]):
#             nozipcount += 1
#         else:
#             yeszipcount += 1
#         print(match)
# print(count1)
# print(count3)
# print(nozipcount)
# print(yeszipcount)