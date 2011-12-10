import subscribers.spacecraft

# Fake IRC Channel
fakeuser = "ircguy42"
botname  = "astrobot"

def fake_client_say(user, message):
  print "%10s | %s" % (user, message)

msl  = subscribers.spacecraft.MSL()
juno = subscribers.spacecraft.Juno()

fake_client_say(fakeuser, "I'm talking in an IRC channel")

fake_client_say(fakeuser, "!msl")
fake_client_say(botname, msl.respond())

fake_client_say(fakeuser, "!juno")
fake_client_say(botname, juno.respond())
