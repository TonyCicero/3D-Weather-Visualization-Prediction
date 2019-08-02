import json
import requests
import sqlite3
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from itertools import chain

#api key
appid = ''  
with open('appid.data', 'r') as file:
    appid = file.read().replace('\n', '')
#USA-48 LAT25~50; LONG -125~-70
startTime = time.time()
cpm = 0
calls = 0
entries = 0
#lonL = -80
#latB = 35
#lonR = -75
#latT = 40
zoom = 10
#http://api.openweathermap.org/data/2.5/box/city?bbox=90,70,50,30,10&appid=09526e5c10271a3d65e467120606b982
#url = "http://api.openweathermap.org/data/2.5/box/city?bbox={0},{1},{2},{3},{4}&appid={5}".format(lonL,latB, lonR, latT, zoom, appid)
#sqlite3 database connection
conn = sqlite3.connect('Weather.db')
c = conn.cursor()
sql_transaction = []

def get_data(lonL,latB,lonR,latT):
    global calls
    global cpm
    global startTime
    global data
    time.sleep(1)
    url = "http://api.openweathermap.org/data/2.5/box/city?bbox={0},{1},{2},{3},{4}&appid={5}".format(lonL,latB, lonR, latT, zoom, appid)    
    response = requests.get(url) 
    data = response.json()
    calls += 1
    cpm = calls/(startTime/60)
    print ("Data calls: ", calls, "CPM: ",cpm)
   
def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS weather 
              (location TEXT PRIMARY KEY, Lat INT, Lon INT,
              temp INT, pressure INT, humidity INT, weatherID INT, fetchTime INT)""")

def sql_insert_data(loc, lat, lon, tmp, pres, humi, wid, ftime):
    try:
        sql = """INSERT INTO weather (location, Lat, Lon, temp, pressure, humidity, weatherID, fetchTime) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}"); """.format(loc, lat, lon, tmp, pres, humi, wid, ftime)
        transaction_bldr(sql)
    except Exception as e:
        print('Data Insertion', e)
        
def transaction_bldr(sql):
    global entries
    entries += 1
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) >= 100:
        print (entries)
        c.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                c.execute(s)
            except Exception as e:
                #print("Transaction: ", e)
                pass
        conn.commit()
        sql_transaction = []

def draw_map(m, scale=0.2):
    # draw a shaded-relief image
    m.bluemarble()
    
    # lats and longs are returned as a dictionary
    lats = m.drawparallels(np.linspace(-90, 90, 13))
    lons = m.drawmeridians(np.linspace(-180, 180, 13))

    # keys contain the plt.Line2D instances
    lat_lines = chain(*(tup[1][0] for tup in lats.items()))
    lon_lines = chain(*(tup[1][0] for tup in lons.items()))
    all_lines = chain(lat_lines, lon_lines)
    
    # cycle through these lines and set the desired style
    for line in all_lines:
        line.set(linestyle='-', alpha=0.3, color='w')

fig = plt.figure(figsize=(20, 20), edgecolor='w')
m = Basemap(projection='cyl', resolution=None,
            llcrnrlat=-90, urcrnrlat=90,
            llcrnrlon=-180, urcrnrlon=180, )
draw_map(m)



#print data["list"][0]["name"]   #location name
#print data["list"][0]["coord"]["Lat"]   #Latitude
#print data["list"][0]["coord"]["Lon"]   #Longitude
#print data["list"][0]["main"]["temp"]   #temperature (in celsius)
#print data["list"][0]["main"]["pressure"]   #pressure
#print data["list"][0]["main"]["humidity"]   #humidity
#print data["list"][0]["weather"][0]["id"]   #Weather id
#print time.time()


#print count
#create_table()


x = -180
y = -90
for y in range(-90,90,5):
    for x in range(-180,180,5):
        get_data(x,y,x+5,y+5)
        
        if data:
            count = data["cnt"]
            for i in range(count):
                #print ("test")
                loc = data["list"][i]["name"]   #location name
                lat = data["list"][i]["coord"]["Lat"]   #Latitude
                lon = data["list"][i]["coord"]["Lon"]   #Longitude
                temp = data["list"][i]["main"]["temp"]   #temperature (in celsius)
                pressure = data["list"][i]["main"]["pressure"]   #pressure
                humidity = data["list"][i]["main"]["humidity"]   #humidity
                w_ID = data["list"][i]["weather"][0]["id"]   #Weather id
                plt.plot(lon, lat, 'ok', markersize=1,color='r')
                #plt.text(lon, lat, loc, fontsize=12);
                sql_insert_data(loc, lat, lon, temp, pressure, humidity, w_ID, time.time())
        

conn.close()
