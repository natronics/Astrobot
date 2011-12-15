import json
import ephem
import datetime
from redis import Redis
import IRC.bot as Bot
import math
from math import sin
from math import cos
from math import tan
import time

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
    
    if m == 60:
      h = h + 1
      m = 0
    
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
    
    if m == 60:
      h = h + 1
      m = 0
      
    return "Next sunrise: %s (%d hours %0.0f minutes from now)" % (time, h, m)
 
  def sun_today(self):
    today = datetime.date.today()
    now = datetime.datetime(today.year,today.month,today.day,8,0,0)
    self.observer.date = now
    sunrise   = ephem.localtime(self.observer.next_rising( self.sun))
    sunset    = ephem.localtime(self.observer.next_setting(self.sun))
    transit   = ephem.localtime(self.observer.next_transit(self.sun))
    
    sunrise_time   = sunrise.strftime("%I:%M:%S %p").lower()
    sunset_time    = sunset.strftime( "%I:%M:%S %p").lower()
    transit_time   = transit.strftime("%I:%M:%S %p").lower()

    sunlight = (sunset - sunrise).seconds / 3600.0
    
    symbol = unichr(0x2609)
    
    return "%s Rise: %s, Noon: %s, Set: %s. %0.2f hours of sunlight" % (symbol, sunrise_time, transit_time, sunset_time, sunlight)
  
  def moon(self):
    today = datetime.date.today()
    now = datetime.datetime(today.year,today.month,today.day,8,0,0)
    self.observer.date = now
    
    moon = ephem.Moon()
    
    moonrise   = ephem.localtime(self.observer.next_rising( moon))
    moonset    = ephem.localtime(self.observer.next_setting(moon))
    transit    = ephem.localtime(self.observer.next_transit(moon))
    
    moonrise_time  = moonrise.strftime("%I:%M:%S %p").lower()
    moonset_time   =  moonset.strftime("%I:%M:%S %p").lower()
    transit_time   =  transit.strftime("%I:%M:%S %p").lower()
    
    phase = ephem.Moon(datetime.datetime(today.year,today.month,today.day,22,0,0)).moon_phase * 100
    
    symbol = unichr(0x263E)
    
    return "%s Rise: %s, Transit: %s, Set: %s. %0.0f%% Illuminated" % (symbol, moonrise_time, transit_time, moonset_time, phase)
    
  def map_range(self, out_low, out_high, range_low, range_high, val):
    a = float(out_high - out_low) / float(range_high - range_low)
    b = out_low - a * range_low
    if val < range_low:
      return out_low
    if val > range_high:
      return out_high
    return (a * val) + b
  
  def day(self):
    now = datetime.date.today()
    self.observer.date = now
    length = 40
    
    sunrise   = ephem.localtime(self.observer.next_rising(self.sun))
    sunset    = ephem.localtime(self.observer.next_setting(self.sun))
    
    
    sunrise = (sunrise.hour + (sunrise.minute / 60.0) + (sunrise.second / 3660.0))
    sunset  = (sunset.hour  + (sunset.minute  / 60.0) + (sunset.second  / 3660.0))
    
    sunlight = sunset - sunrise
    sunlight_hours = sunlight
    
    # Graph
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

    return "%0.2f hours of sunlight today: %s" % (sunlight_hours, graph)

  def planet(self, planet):
    today = datetime.date.today()
    now = datetime.datetime(today.year,today.month,today.day,8,0,0)

    rise    = ephem.localtime(self.observer.next_rising( planet))
    sset    = ephem.localtime(self.observer.next_setting(planet))
    transit = ephem.localtime(self.observer.next_transit(planet))
    
    rise_time    =     rise.strftime("%I:%M:%S %p").lower()
    set_time     =     sset.strftime("%I:%M:%S %p").lower()
    transit_time =  transit.strftime("%I:%M:%S %p").lower()
    
    constellation = ephem.constellation(planet)[1].lower()
    
    return rise_time, set_time, transit_time, constellation

  def venus(self):
    rise_time, set_time, transit_time, constellation = self.planet(ephem.Venus())
    symbol = unichr(0x2640)
    return "%s Rise: %s, Transit: %s, Set: %s. In the constellation %s" % (symbol, rise_time, set_time, transit_time, constellation)
    
  def mars(self):
    rise_time, set_time, transit_time, constellation = self.planet(ephem.Mars())
    symbol = unichr(0x2642)
    return "%s Rise: %s, Transit: %s, Set: %s. In the constellation %s" % (symbol, rise_time, set_time, transit_time, constellation)
  
  def jupiter(self):
    rise_time, set_time, transit_time, constellation = self.planet(ephem.Jupiter())
    symbol = unichr(0x2643)
    return "%s Rise: %s, Transit: %s, Set: %s. In the constellation %s" % (symbol, rise_time, set_time, transit_time, constellation)
  
  def saturn(self):
    rise_time, set_time, transit_time, constellation = self.planet(ephem.Saturn())
    symbol = unichr(0x2644)
    return "%s Rise: %s, Transit: %s, Set: %s. In the constellation %s" % (symbol, rise_time, set_time, transit_time, constellation)
  
  def uranus(self):
    rise_time, set_time, transit_time, constellation = self.planet(ephem.Uranus())
    symbol = unichr(0x2645)
    return "%s Rise: %s, Transit: %s, Set: %s. In the constellation %s" % (symbol, rise_time, set_time, transit_time, constellation)
  
  def neptune(self):
    rise_time, set_time, transit_time, constellation = self.planet(ephem.Neptune())
    symbol = unichr(0x2646)
    return "%s Rise: %s, Transit: %s, Set: %s. In the constellation %s" % (symbol, rise_time, set_time, transit_time, constellation)

  def localtime(self):
    now = datetime.datetime.utcnow()
    self.observer.date = now
    time = ephem.localtime(self.observer.date)
    
    tz = "PST"
    
    if ((now - time).seconds / 3600) < 8:
      tz = "PDT"
    
    return "          Localtime:  %s %s" % (time.strftime("%I:%M:%S %p").lower(), tz)

  def utc(self):
    now = datetime.datetime.utcnow()
    return "                UTC:  %s" % now.strftime("%H:%M:%S")

  def unixtime(self):
    now = time.time()
    return "           unixtime:  %0.0f" % now
  
  def jd(self):
    now = datetime.datetime.utcnow()
    JD = ephem.julian_date(now)
    return "         Julian Day:  %s" % JD
  
  def solar_time(self):
    now         = datetime.datetime.utcnow()
    perihelion  = datetime.datetime(2011,1,3,19,0,0)
    
    n = (now - perihelion).days + ((now - perihelion).seconds / 86400.0)
    M = (2*math.pi*n)/(365.242)
  
    dt = -7.657*sin(M) + 9.862*sin(2*M + 3.599) # minutes
    
    self.observer.date = now
    time = ephem.localtime(self.observer.date)
    
    solartime = time + datetime.timedelta(minutes=dt)
    
    return "Apparent Solar Time:  %s" % solartime.strftime("%I:%M:%S %p").lower()

  def sidereal_time(self):
    now = datetime.datetime.utcnow()
    self.observer.date = now
    
    time = self.observer.sidereal_time()
    return "      Sidereal Time:  %11s" % time
    
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
        
        if sender != 'ntron' and channel in ['#pdxWebDev', '#pdxbots']:
          if "!sunset" in text.lower():
            Bot.say(channel, self.portland.sunset())
          if "!sunrise" in text.lower():
            Bot.say(channel, self.portland.sunrise())
          if "!daylight" in text.lower():
            Bot.say(channel, self.portland.day())
          if "!sun" in text.lower():
            Bot.say(channel, self.portland.sun_today())
          if "!moon" in text.lower() or "!moonrise" in text.lower() or "!moonset" in text.lower() or "!moonphase" in text.lower():
            Bot.say(channel, self.portland.moon())
          if "!venus " in text.lower():
            Bot.say(channel, self.portland.venus())
          if "!mars" in text.lower():
            Bot.say(channel, self.portland.mars())
          if "!jupiter" in text.lower():
            Bot.say(channel, self.portland.jupiter())
          if "!saturn " in text.lower():
            Bot.say(channel, self.portland.saturn())
          if "!uranus" in text.lower():
            Bot.say(channel, self.portland.uranus())
          if "!neptune" in text.lower():
            Bot.say(channel, self.portland.neptune())
          if "!pluto" in text.lower():
            Bot.say(channel, sender + ": " + "Pluto isn't a planet! >:o")
          if "!time" in text.lower():
            Bot.say(channel, self.portland.localtime())
            Bot.say(channel, self.portland.utc())
            Bot.say(channel, self.portland.solar_time())
            Bot.say(channel, self.portland.sidereal_time())
            Bot.say(channel, self.portland.unixtime())
            Bot.say(channel, self.portland.jd())
