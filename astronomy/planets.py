import ephem
import datetime

portland = ephem.Observer()
portland.lat = "45.51200"
portland.lon = "-122.631007"
portland.elevation = 50

def strfy(dt):
    return dt.strftime("%I:%M:%S %p").lower()


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

    def set_now(self, dt=datetime.datetime.utcnow()):
        self.now = dt

    def set_observer(self, observer):
        self.obsv = observer

    def risetime(self):
        self.obsv.date = self.now
        rise = ephem.localtime(self.obsv.next_rising(self.planet))
        return rise

    def today(self):
        return {'rise': strfy(self.risetime())}


Sol = Planet(ephem.Sun())
