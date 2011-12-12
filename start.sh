#!/bin/bash

# Start all services
start_all ()
{
  start_bot
  start_listen
}

# Start just the IRC bot (nodejs)
start_bot ()
{
  screen -d -m -S nodeIRCbot node ./IRC/bot.js
  echo "Started bot"
}

# Start just the python listeners
start_listen ()
{
  screen -d -m -S nasaListener  python ./listen_nasa.py
  screen -d -m -S astroListener python ./listen_astronomy.py
  echo "Started python"
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Script Arguments:
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if [ ! -n "$1" ]
then
  start_all
else
  if [ $1 = "all" ] 
  then
    start_all
  fi
  if [ $1 = "listen" ] 
  then
    start_listen
  fi
  if [ $1 = "bot" ] 
  then
    start_bot
  fi
fi
