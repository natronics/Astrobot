import subscribers.spacecraft
import subscribers.astronomy

# Fake IRC Channel
fakeuser = "guy42"
botname  = "astrobot"

def fake_client_say(user, message):
  print "%10s | %s" % (user, message)

msl     = subscribers.spacecraft.MSL()
juno    = subscribers.spacecraft.Juno()
pdx     = subscribers.astronomy.Portland()
launch  = subscribers.spacecraft.Launches()

fake_client_say(fakeuser, "I'm talking in an IRC channel")

fake_client_say(fakeuser, "!msl")
fake_client_say(botname, msl.respond())

fake_client_say(fakeuser, "!juno")
fake_client_say(botname, juno.respond())

fake_client_say(fakeuser, "!sunset")
fake_client_say(botname, pdx.sunset())

fake_client_say(fakeuser, "!sunrise")
fake_client_say(botname, pdx.sunrise())

fake_client_say(fakeuser, "!daylight")
fake_client_say(botname, pdx.day())

fake_client_say(fakeuser, "!sun")
fake_client_say(botname, pdx.sun_today())

fake_client_say(fakeuser, "!moon")
fake_client_say(botname, pdx.moon())

fake_client_say(fakeuser, "!mercury")
fake_client_say(botname, pdx.mercury())

fake_client_say(fakeuser, "!venus")
fake_client_say(botname, pdx.venus())

fake_client_say(fakeuser, "!mars")
fake_client_say(botname, pdx.mars())

fake_client_say(fakeuser, "!jupiter")
fake_client_say(botname, pdx.jupiter())
fake_client_say(fakeuser, "!saturn")
fake_client_say(botname, pdx.saturn())
fake_client_say(fakeuser, "!uranus")
fake_client_say(botname, pdx.uranus())
fake_client_say(fakeuser, "!neptune")
fake_client_say(botname, pdx.neptune())
fake_client_say(fakeuser, "!pluto")
fake_client_say(botname, fakeuser + ": " + "Pluto isn't a planet! >:o")

fake_client_say(fakeuser, "!time")
fake_client_say(botname, pdx.localtime())
fake_client_say(botname, pdx.utc())
fake_client_say(botname, pdx.solar_time())
fake_client_say(botname, pdx.sidereal_time())
fake_client_say(botname, pdx.unixtime())
fake_client_say(botname, pdx.jd())

fake_client_say(fakeuser, "!falcon")
fake_client_say(botname, launch.launch("falcon9-cots23"))

fake_client_say(fakeuser, "!soyuz")
fake_client_say(botname, launch.launch("SoyuzTMA-03M"))
