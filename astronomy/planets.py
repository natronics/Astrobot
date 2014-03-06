import ephem
import pytz
import datetime

portland = ephem.Observer()
portland.lat = "45.51200"
portland.lon = "-122.631007"
portland.elevation = 50

local_tz = pytz.timezone('US/Pacific')


def strfy(dt):
    if dt.second > 30:
        dt.replace(minutes=(dt.minute + 1))
    return dt.strftime("%a %I:%M %p").lower()


class Planet(object):
    """ Represent a planet

    :param object planet: the planet object
    :returns: a Planet instance
    """

    def __init__(self, planet):
        self.planet = planet

        # defaults
        self.now = datetime.datetime.utcnow()
        self.obsv = portland

    def set_now(self, dt=datetime.datetime.utcnow().replace(tzinfo=pytz.utc)):
        local = dt.astimezone(local_tz)
        self.now = datetime.datetime(local.year, local.month, local.day, dt.hour, dt.minute, dt.second)

    def set_observer(self, observer):
        self.obsv = observer

    def risetime(self):
        self.obsv.date = self.now
        rise = (self.obsv.next_rising(self.planet)).datetime()
        rise = rise.replace(tzinfo=pytz.utc)
        return rise

    def today(self):
        return {'rise': strfy(self.risetime().astimezone(local_tz)
)}


Sol = Planet(ephem.Sun())
