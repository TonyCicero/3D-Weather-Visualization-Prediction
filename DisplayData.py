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

SA = [20,60,-90,-65] #StudyArea- minLat,maxLat,minLon,maxLon

TimeRange = [1565751859.9466648,1565751900]

cm = plt.cm.get_cmap('bwr')

plt.figure()

lat = []
lon = []
data = []

def GetData():
    conn = sqlite3.connect('EastCoast.db')
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
    
    fig = plt.figure(figsize=(20, 20), edgecolor='w')
    m = Basemap(projection='cyl', resolution=None,
                    llcrnrlat=SA[0], urcrnrlat=SA[1],
                    llcrnrlon=SA[2], urcrnrlon=SA[3], )
    
    
        
        #print(data)
    sc = plt.scatter(lon, lat, c=data, cmap=cm, s=50,alpha=1)
    plt.colorbar(sc)
    plt.suptitle('US East Coast Atmospheric Pressure - {0}'.format(datetime.fromtimestamp(TimeRange[0])), fontsize=20)
    draw_map(m)
    plt.savefig('images/EastCoast_{0}-{1}.png'.format(TimeRange[0],TimeRange[1]))
