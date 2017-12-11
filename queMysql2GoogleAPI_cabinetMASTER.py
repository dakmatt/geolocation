#!/usr/bin/python
## author: ahmad fairuz ali 
## date : 16 July 2014 
## script ini bertujuan untuk mengambil latitude dan longitude berdasarkan lokasi yang telah ditetapkan 
## happy using it 
# http://www.indjango.com/google-api-to-get-lat-long-data/



import MySQLdb
import cx_Oracle
import string
import datetime
import requests

## menjelaskan connection to oracle 
oraconstring='YOURID/YOURPASSWORD@YOURURL:1521/YOURSCHEMA'
ora_conn = cx_Oracle.connect(oraconstring)
ora_cursor = ora_conn.cursor()

## menjelaskan connection to mysql pulak
mysql_conn = MySQLdb.connect("localhost","YOURID","YOURPASSWORD","YOURDATABASENAME" )
mysql_cursor = mysql_conn.cursor()

tablename = 'result_latlng_cabinetJohorNew'
sourcetable = 'cabinet_JOHOR'
try:
    selectstring="""select CABINET_ADDR from """ + sourcetable + """ where checkstat is null"""
    mysql_cursor.execute(selectstring)
except:
   print "failed to select from mysql "

## mapped kan dengan result set 
Resultset_my_List=[]

for (ADDRESS) in mysql_cursor:
   try:
	Resultset_my_List.append((ADDRESS))
   except AttributeError:
	pass 

#print Resultset_my_List
print str(len(Resultset_my_List)) + ' Records from MYSQL'

## shooting to ORACLE SQL lak 

Resultset_Geocoding_List = []
count=0
##  source data dari oracle 
try:
    for (ADDRESS) in Resultset_my_List:
	count=count+1
	newAddress = ''.join(ADDRESS)
	newAddress.replace(' ','')
	print 'new address yg dicari' + newAddress
	try:
	    api_key = "" # put your own API KEY , can get from developer
	    api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(ADDRESS, api_key))
	    api_response_dict = api_response.json()
	    if api_response_dict['status'] == 'OK':
		latitude = api_response_dict['results'][0]['geometry']['location']['lat']
		longitude = api_response_dict['results'][0]['geometry']['location']['lng']
		print 'Latitude:', latitude
		print 'Longitude:', longitude
	    Resultset_Geocoding_List.append([latitude,longitude])
        except AttributeError:
            pass
	print 'result yg ke' + str(count)
	print 'Before ' + str(Resultset_Geocoding_List)
        if Resultset_Geocoding_List:
            for row in Resultset_Geocoding_List:
                row.insert(0,newAddress)
            print 'Insert if value found ' + str(Resultset_Geocoding_List)
            insertMysqlString1="""INSERT INTO """ + tablename + """ (ADDRESS,LATITUDE,LONGITUDE) values(%s,%s,%s) """
            mysql_cursor.executemany(insertMysqlString1,Resultset_Geocoding_List)
	    print insertMysqlString1
            mysql_conn.commit()
	    insertMysqlString2="""UPDATE """ + sourcetable + """ set checkstat='1' """
	    print insertMysqlString2
            mysql_cursor.execute(insertMysqlString2)
	    mysql_conn.commit()
	else:
            Resultset_Geocoding_List[0]=newAddress
            Resultset_Geocoding_List[1]='not found'
            Resultset_Geocoding_List[2]='not found'
            print 'Insert if value not found ' + str(Resultset_Geocoding_List)
            insertMysqlString3=""" INSERT INTO """ + tablename + """(ADDRESS,LATITUDE,LONGITUDE) values(%s,%s,%s) """
	    print insertMysqlString3
	    mysql_cursor.executemany(insertMysqlString3,Resultset_Geocoding_List)
	    mysql_conn.commit()
	    insertMysqlString4=""" UPDATE """ + sourcetable + """  set checkstat='1' """
	    print insertMysqlString4
            mysql_cursor.execute(insertMysqlString4)
            mysql_conn.commit()
	del Resultset_Geocoding_List[:]
except AttributeError:
	print 'error found geocoding'
	pass

print Resultset_Geocoding_List
print str(count) + ' Records from DWHDB' 
## checking berapa banyak yg dah masuk
checkingstring = """ select count(*) from """ + tablename
mysql_cursor.execute(checkingstring)
mysql_row_count= mysql_cursor.fetchone()
print str(mysql_row_count[0]) + ' Records inserted into mysql'

## closing....

mysql_cursor.close()
ora_cursor.close()


