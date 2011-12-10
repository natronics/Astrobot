import ephem
import datetime
import telnetlib
import os

datafile = os.path.abspath("data/spacecraft.json")

class ephem_util(object):
  
  @staticmethod
  def unit_order(n):
    unit = ""
    if n > 0.5e4:
      unit = 'thousand'
      n = n/1000.0
    
    if n > 900:
      unit = 'million'
      n = n/1.0e3
      
    if n > 300:
      unit = 'billion'
      n = n/1.0e3
    
    return (unit, n)
  
  @staticmethod
  def unit_time(n):
    unit = "seconds"
    if n > 90:
      unit = 'minutes'
      n = n/60.0
    
    if n > 90:
      unit = 'hours'
      n = n/60.0
      
    if n > 48:
      unit = 'days'
      n = n/24.0
    
    return (unit, n)
  
  @staticmethod
  def progress_bar(percent):
    total = 10
    sofar = int(round(percent/10.0))
    togo  = total - sofar

    progress = "[%s%s] %0.1f%%" % (("=" * sofar), (" " * togo), percent)

    return progress
  
  @staticmethod
  def make_ephem_object(elements):
  
    e = {}
    if elements['Elements']['Eccentricity'] < 1:
      e = ephem.EllipticalBody()
    
    e.name        = elements['name']
    e._inc        = elements['Elements']['Inclination']
    e._Om         = elements['Elements']['LAAN']
    e._om         = elements['Elements']['Argument_of_Periapsis']
    e._a          = elements['Elements']['Semimajor_Axis']
    e._e          = elements['Elements']['Eccentricity']
    e._M          = elements['Elements']['Mean_Anomaly']
    epoch_date    = elements['Elements']['Epoch'] - 2415020 # JD to DJD
    
    e._epoch_M    = ephem.Date(epoch_date)
    e._epoch      = ephem.Date('2000/1/1')
    
    return e

class Horizons(object):

  HOST = "horizons.jpl.nasa.gov"
  PORT = 6775
  ESC = chr(0x1b)
  
  def __init__(self):
    self.now = datetime.datetime.utcnow()
    self.now_str = self.now.strftime('%Y-%b-%d %H:%M')
    next = self.now + datetime.timedelta(0,3600)
    self.next_str = next.strftime('%Y-%b-%d %H:%M')
    
    self.OE_tree = [('<cr>:',               'E\n')                  # Ephemeris
              , ('[o,e,v,?] :',             'e\n')                  # Elements
              , ('[ ###, ? ] :',            '500@10\n')             # Sol body center
              , ('[ y/n ] -->',             'y\n')                  # Confirm
              , ('[eclip, frame, body ] :', 'eclip\n')              # Frame Coords
              , ('] :',                     "%s\n" % self.now_str)  # Begin Time
              , ('] :',                     "%s\n" % self.next_str) # End Time
              , ('? ] :',                   '1d\n')                 # Interval
              , ('?] :',                    'n\n')                  # Defaults?
              , ('[J2000, B1950] :',        'J2000\n')              # J2000 Coords
              , ('3=KM-D] :',               '2\n')                  # AU units
              , ('YES, NO ] :',             'YES\n')                # CSV
              , ('YES, NO ] :',             'NO\n')                 # No labels
              , ('ABS, REL ] :',            'ABS\n')]               # Absolute time

  def get_orbital_elements(self, code):
    
    telnet = telnetlib.Telnet(self.HOST, self.PORT)

    # Debug:
    #telnet.set_debuglevel(10)
    
    print 'Waiting for Horizons...'

    telnet.read_until('Horizons>')
    telnet.write("%s\n" % code)

    for cue in self.OE_tree:
      telnet.read_until(cue[0])
      telnet.write(cue[1])
    
    elements = telnet.read_until('$$EOE')
    elements = elements.split('$$SOE')[1]
    elements = elements.strip('$$EOE')
    
    print "Processing Responce..."
    
    #  0    1   2   3   4   5   6   7  8  9   10 11  12  13
    #JDCT ,   , EC, QR, IN, OM, W, Tp, N, MA, TA, A, AD, PR
    
    """
      JDCT     Epoch Julian Date, Coordinate Time
      EC     Eccentricity, e                                                   
      QR     Periapsis distance, q (AU)                                        
      IN     Inclination w.r.t xy-plane, i (degrees)                           
      OM     Longitude of Ascending Node, OMEGA, (degrees)                     
      W      Argument of Perifocus, w (degrees)                                
      Tp     Time of periapsis (Julian day number)                             
      N      Mean motion, n (degrees/day)                                      
      MA     Mean anomaly, M (degrees)                                         
      TA     True anomaly, nu (degrees)                                        
      A      Semi-major axis, a (AU)                                           
      AD     Apoapsis distance (AU)                                            
      PR     Orbital period (day)   
    """
    
    elements = elements.split(',')
    
    EpochJD               = float(elements[0])
    Eccentricity          = float(elements[2])
    Inclination           = float(elements[4])
    LAAN                  = float(elements[5])
    Argument_of_Periapsis = float(elements[6])
    Mean_Anomaly          = float(elements[9])
    Semimajor_Axis        = float(elements[11])
    
    e_dict = {"Epoch": EpochJD, "Eccentricity": Eccentricity
                      , "Inclination": Inclination, "LAAN": LAAN
                      , "Argument_of_Periapsis": Argument_of_Periapsis
                      , "Mean_Anomaly": Mean_Anomaly
                      , "Semimajor_Axis": Semimajor_Axis }
    
    telnet.close()
    
    return e_dict
