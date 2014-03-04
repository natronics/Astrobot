import json
from zenircbot_api import ZenIRCBot

# default redis server, future behavior will get config from python api
zen = ZenIRCBot('localhost', 6379, 0)

@zen.simple_command('ping', desc="respond to a person")
def test(message):
    return 'pongo'

zen.listen()
