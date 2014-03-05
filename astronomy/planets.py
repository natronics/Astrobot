

class Planet(object):
    """ Represent a planet

    :param object planet: the planet object
    :returns: a Planet instance
    """

    def __init__(self, planet):
        self.planet = planet


    def risetime(self):
        return "08:15"


    def today(self):
        return {'rise': self.risetime()}

Sol = Planet("the sun")
