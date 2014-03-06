#!/usr/bin/env python
import json
from astronomy import planets
from zenircbot_api import ZenIRCBot

# default redis server, future behavior will get config from python api
zen = ZenIRCBot('localhost', 6379, 0)

@zen.simple_command('sun', desc="compute sun angle, rise, set, etc.")
def sun(message):

    sol = planets.Sol
    sol.set_now()
    info = planets.Sol.today()
    return 'rise: '+info['rise']


if __name__ == '__main__':
    zen.listen()
