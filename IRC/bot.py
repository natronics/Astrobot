from redis import Redis
import json

def say(channel, message):
  Redis().publish('astrobot-toIRC',
                  json.dumps({
              'version': 1,
              'type': 'privmsg',
              'data': {
                  'to': channel,
                  'message': message,
                  }
              }))
