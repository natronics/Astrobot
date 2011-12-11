import json
import ephem
import datetime
import data.util as Util
from redis import Redis
import IRC.bot as Bot

class spacecraft_listener(object):
  
  def __init__(self):
    self.redis = Redis()
    self.redis.subscribe(['astrobot-fromIRC'])
    
    self.msl    = MSL()
    self.juno   = Juno()
  
  def listen(self):
    for blob in self.redis.listen():
      if blob['type'] == "message":
        data    = json.loads(blob['data'])
        print data
        sender  = data['data']['sender']
        channel = data['data']['channel']
        text    = data['data']['message']
        
        if sender != 'ntron':
          if "!msl" in text.lower():
            Bot.say(channel, self.msl.respond())
          elif "!juno" in text.lower():
            Bot.say(channel, self.juno.respond())
          
    
class spacecraft(object):
  
  def compute(self, s):
    now = datetime.datetime.utcnow()
    s.compute(now)
    
    d_m = s.earth_distance * ephem.meters_per_au
    km_units, d_km = Util.ephem_util.unit_order(d_m / 1000.0)
    
    d_lt = d_m / ephem.c
    lt_units, d_lt = Util.ephem_util.unit_time(d_lt)

    since_launch = (now - self.launch)
    since_launch_s = since_launch.days * 86400 + since_launch.seconds
    
    togo = (self.arrive - now)
    togo_s = togo.days * 86400 + togo.seconds
    precent = since_launch_s / float(togo_s + since_launch_s)
    precent = precent*100

    progress = Util.ephem_util.progress_bar(precent)
    
    self.message_data = (d_km, km_units, d_lt, lt_units, progress, togo.days)
    
class MSL(spacecraft):

  def __init__(self):
    self.launch = datetime.datetime(2011,11,26,15,2,0)
    self.data          = {}
    self.arrive        = {}
    self.message_data  = ()
  
  def respond(self):
    # Read data
    self.data   = json.loads(open(Util.datafile, 'r').read())['msl']
    self.arrive = datetime.datetime.strptime(self.data['arrival_date'], "%Y-%m-%dT%H:%M:%S")
    
    # Put data in ephem
    msl = Util.ephem_util.make_ephem_object(self.data)
    
    # Compute values
    self.compute(msl)
    
    return "MSL is %1.2f %s km from Earth (%0.1f light %s)  %s to Mars (%d days to go)" % self.message_data

class Juno(spacecraft):
  
  def __init__(self):
    self.launch = datetime.datetime(2011,8,5,16,25,0)
    self.data          = {}
    self.arrive        = {}
    self.message_data  = ()

  def respond(self):
    # Read data
    self.data   = json.loads(open(Util.datafile, 'r').read())['juno']
    self.arrive = datetime.datetime.strptime(self.data['arrival_date'], "%Y-%m-%dT%H:%M:%S")
    
    # Put data in ephem
    msl = Util.ephem_util.make_ephem_object(self.data)
    
    # Compute values
    self.compute(msl)
    
    return "Juno is %1.2f %s km from Earth (%0.1f light %s) %s to Jupiter (%d days to go)" % self.message_data
