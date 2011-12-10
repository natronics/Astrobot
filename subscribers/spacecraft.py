import json
import ephem
import datetime
import data.util as Util



class spacecraft(object):

  def compute(self, s, launch, arrive):
    now = datetime.datetime.utcnow()
    s.compute(now)
    
    d_m = s.earth_distance * ephem.meters_per_au
    km_units, d_km = Util.ephem_util.unit_order(d_m / 1000.0)
    
    d_lt = d_m / ephem.c
    lt_units, d_lt = Util.ephem_util.unit_time(d_lt)

    since_launch = (now - launch)
    since_launch_s = since_launch.days * 86400 + since_launch.seconds
    
    togo = (arrive - now)
    togo_s = togo.days * 86400 + togo.seconds
    precent = since_launch_s / float(togo_s + since_launch_s)
    precent = precent*100

    progress = Util.ephem_util.progress_bar(precent)
    
    return (d_km, km_units, d_lt, lt_units, progress, togo.days)
    
class MSL(spacecraft):
  
  launch_dt = datetime.datetime(2011,11,26,15,2,0)
  
  def respond(self):
    data = json.loads(open(Util.datafile, 'r').read())['msl']
    
    msl = Util.ephem_util.make_ephem_object(data)
    arrival_dt = datetime.datetime.strptime(data['arrival_date'], "%Y-%m-%dT%H:%M:%S")
    
    message_data = self.compute(msl, self.launch_dt, arrival_dt)
    
    return "MSL is %1.2f %s km from Earth (%0.1f light %s)  %s to Mars (%d days to go)" % message_data

class Juno(spacecraft):
  
  launch_dt = datetime.datetime(2011,8,5,16,25,0)
  
  def respond(self):
    data = json.loads(open(Util.datafile, 'r').read())['juno']
    
    juno = Util.ephem_util.make_ephem_object(data)
    arrival_dt = datetime.datetime.strptime(data['arrival_date'], "%Y-%m-%dT%H:%M:%S")
    
    message_data = self.compute(juno, self.launch_dt, arrival_dt)
    
    return "Juno is %1.2f %s km from Earth (%0.1f light %s) %s to Jupiter (%d days to go)" % message_data
