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
    
    sunrise = self.observer.next_rising(self.sun)
    
    localtime = ephem.localtime(sunrise)
    
    time = localtime.strftime("%I:%M:%S %p").lower()
    diff = (sunrise.datetime() - now)
    diff = diff.days*86400 + diff.seconds
    
    h = int(math.floor(diff / 3600.0))
    m = int(round((diff - (h*3600)) / 60.0))
    
    return "Next sunrise: %s (%d hours %0.0f minutes from now)" % (time, h, m)
    
  def map_range(self, out_low, out_high, range_low, range_high, val):
    a = float(out_high - out_low) / float(range_high - range_low)
    b = out_low - a * range_low
    if val < range_low:
      return out_low
    if val > range_high:
      return out_high
    return (a * val) + b
  
  def day(self):
    now = datetime.datetime.utcnow()
    self.observer.date = now
    length = 40
    
    sunrise   = ephem.localtime(self.observer.next_rising(self.sun))
    sunset    = ephem.localtime(self.observer.next_setting(self.sun))
    
    
    sunrise = (sunrise.hour + (sunrise.minute / 60.0) + (sunrise.second / 3660.0))
    sunset  = (sunset.hour  + (sunset.minute  / 60.0) + (sunset.second  / 3660.0))
    
    sunlight = sunset - sunrise

    """    
    sunrise  = int(round(self.map_range(0, length, 0, 24, sunrise)))
    sunset   = int(round(self.map_range(0, length, 0, 24, 24-  sunset)))
    sunlight = int(round(self.map_range(0, length, 0, 24, sunlight)))

    graph  = "["
    graph += " " * (sunrise - 1)
    graph += unichr(0x2591)
    graph += unichr(0x2593)
    
    graph += unichr(0x2588) * (sunlight - 2)
    
    graph += unichr(0x2593)
    graph += unichr(0x2591)
    
    graph += " " * (sunset - 1)
    graph += "]"
    print  "  astrobot | [1234567890123456789012345678901234567890]"
    """
    return "There are %0.2f hours of sunlight today" % sunlight

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
          if "!daylight" in text.lower():
            Bot.say(channel, self.portland.day())
