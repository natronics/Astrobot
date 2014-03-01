import json
from zenircbot_api import ZenIRCBot

# default redis server, future behavior will get config from python api
zen = ZenIRCBot('localhost', 6379, 0)


@zen.simple_command('route')
def test(message):
    return "fire"

@zen.simple_command('echoo', desc="echo's the part after 'echo'")
def test(message):
    return message.split('echoo')[1].strip()

zen.listen()
