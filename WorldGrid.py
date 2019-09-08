
SA = [-90,90,-180,180] #StudyArea- minLat,maxLat,minLon,maxLon
Scale = 1 #grid in degrees

class node:
    def __init__(self, temp, pressure, humidity, wid):
        self.temp = temp
        self.pressure = pressure
        self.humidity = humidity
        self.wid = wid
        
        
def init_Grid:
    