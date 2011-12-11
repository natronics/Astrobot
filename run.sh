#!/bin/bash

# Start Bot
screen -d -m -S nodeIRCbot node ./IRC/bot.js

# Listnen to space triggers
screen -d -m -S spaceListener python ./listen_space.py
