import subscribers.spacecraft
import subscribers.astronomy

# Fake IRC Channel
fakeuser = "ircguy42"
botname  = "astrobot"

def fake_client_say(user, message):
  print "%10s | %s" % (user, message)

msl   = subscribers.spacecraft.MSL()
juno  = subscribers.spacecraft.Juno()
pdx   = subscribers.astronomy.Portland()

fake_client_say(fakeuser, "I'm talking in an IRC channel")

fake_client_say(fakeuser, "!msl")
fake_client_say(botname, msl.respond())

fake_client_say(fakeuser, "!juno")
fake_client_say(botname, juno.respond())

fake_client_say(fakeuser, "!sunset")
fake_client_say(botname, pdx.sunset())

fake_client_say(fakeuser, "!sunrise")
fake_client_say(botname, pdx.sunrise())
