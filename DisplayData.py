import json
import requests
import sqlite3
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from itertools import chain
from datetime import datetime
from mpl_toolkits.axes_grid1 import make_axes_locatable


SA = [-90,90,-180,180] #StudyArea- minLat,maxLat,minLon,maxLon

TimeRange = [1566052220.1170807,1566055327.5714192]

cm = plt.cm.get_cmap('seismic')

plt.figure()

lat = []
lon = []
data = []


def GetData():
    conn = sqlite3.connect('WorldWeather.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM weather WHERE fetchTime >= ? AND fetchTime <= ?;", (TimeRange[0],TimeRange[1]))
     
    rows = c.fetchall()
    for row in rows:
        lat.append(row[1])
        lon.append(row[2])
        data.append(row[4])

    
def draw_map(m, scale=0.2):
    global SA
    # draw a shaded-relief image
    m.bluemarble()
        
    # lats and longs are returned as a dictionary
    lats = m.drawparallels(np.linspace(SA[0], SA[1], 13))
    lons = m.drawmeridians(np.linspace(SA[2], SA[3], 13))
    
    # keys contain the plt.Line2D instances
    lat_lines = chain(*(tup[1][0] for tup in lats.items()))
    lon_lines = chain(*(tup[1][0] for tup in lons.items()))
    all_lines = chain(lat_lines, lon_lines)
    
def GenMap(t1,t2):
    TimeRange[0] = t1
    TimeRange[1] = t2
    GetData()
    
    fig = plt.figure(figsize=(30, 30), edgecolor='w')
    m = Basemap(projection='cyl', resolution=None,
                    llcrnrlat=SA[0], urcrnrlat=SA[1],
                    llcrnrlon=SA[2], urcrnrlon=SA[3], )
    
    
        
        #print(data)
    
    sc = plt.scatter(lon, lat, c=data, cmap=cm, s=5,alpha=1)
    ax = plt.gca()
    
    plt.colorbar(sc,fraction=.02)
    plt.suptitle('World Atmospheric Pressure (millibars) - {0}'.format(datetime.fromtimestamp(TimeRange[0])), fontsize=20)
    draw_map(m)
    plt.savefig('images/World_{0}-{1}.png'.format(TimeRange[0],TimeRange[1]))
    print("Done Creating Map: {0}".format(time.time()))
    
GenMap(TimeRange[0],TimeRange[1])