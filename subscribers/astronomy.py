import json
import ephem
import datetime
from redis import Redis
import IRC.bot as Bot
import math

class Portland(object):
  
  lat = "45.51200"
  lon = "-122.631007"
  alt = 15
  
  def __init__(self):
     self.observer = ephem.Observer()
     self.observer.lon        = self.lon
     self.observer.lat        = self.lat
     self.observer.elevation  = self.alt
     
     self.sun = ephem.Sun()

  def sunset(self):
    now = datetime.datetime.utcnow()
    self.observer.date = now
    
    sunset = self.observer.next_setting(self.sun)
    
    localtime = ephem.localtime(sunset)
    
    time = localtime.strftime("%I:%M:%S %p").lower()
    diff = (sunset.datetime() - now)
    diff = diff.days*86400 + diff.seconds
    
    h = int(math.floor(diff / 3600.0))
    m = int(round((diff - (h*3600)) / 60.0))
    
    return "Next sunset: %s (%d hours %0.0f minutes from now)" % (time, h, m)


  def sunrise(self):
    now = datetime.datetime.utcnow()
    self.observer.date = now
    
    sunset = self.observer.next_rising(self.sun)
    
    localtime = ephem.localtime(sunset)
    
    time = localtime.strftime("%I:%M:%S %p").lower()
    diff = (sunset.datetime() - now)
    diff = diff.days*86400 + diff.seconds
    
    h = int(math.floor(diff / 3600.0))
    m = int(round((diff - (h*3600)) / 60.0))
    
    return "Next sunrise: %s (%d hours %0.0f minutes from now)" % (time, h, m)
    
class portland_listener(object):
  
  def __init__(self):
    self.redis = Redis()
    self.redis.subscribe(['astrobot-fromIRC'])
    
    self.portland = Portland()
  
  def listen(self):
    for blob in self.redis.listen():
      if blob['type'] == "message":
        data    = json.loads(blob['data'])
        print data
        sender  = data['data']['sender']
        channel = data['data']['channel']
        text    = data['data']['message']
        
        if sender != 'ntron':
          if "!sunset" in text.lower():
            Bot.say(channel, self.portland.sunset())
          if "!sunrise" in text.lower():
            Bot.say(channel, self.portland.sunrise())
