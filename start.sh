#!/bin/bash

# Start Bot
screen -d -m -S nodeIRCbot node ./IRC/bot.js

# Listnen to space triggers
screen -d -m -S nasaListener python ./listen_nasa.py
screen -d -m -S astroListener python ./listen_astronomy.py
