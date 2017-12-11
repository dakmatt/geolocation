#!/usr/bin/python
# author: ahmad fairuz ali 
# datea : 11 september 2016 
# script ini bertujuan untuk mengambil lat dan long , dengan process invocationnya dartang dari R menggunakan rPython 

# 
#

import string
import datetime
import requests

ADDRESS = "BLOK 5 UKAY BAYU,UKAY HEIGHTS,AMPANG"
#ADDRESS = "APARTMENT PERMAI PUTERI,TAMAN DATO AHMAD RAZALI,AMPANG"
#ADDRESS = "APARTMENT MESRA PRIMA,	IKAN EMAS,	TAMAN PANDAN MESRA	,AMPANG"
#ADDRESS = "AMPANG SAUJANA,AMPANG "
api_key = ""
api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(ADDRESS, api_key))
api_response_dict = api_response.json()
if api_response_dict['status'] == 'OK':
    latitude = api_response_dict['results'][0]['geometry']['location']['lat']
    longitude = api_response_dict['results'][0]['geometry']['location']['lng']
    print 'Latitude:', latitude
    print 'Longitude:', longitude
