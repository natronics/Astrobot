#!/bin/bash

# Stop all services
stop_all ()
{
  stop_bot
  stop_listen
}

# Stop just the IRC bot (nodejs)
stop_bot ()
{
  screen -S nodeIRCbot -X quit
  echo "Stopped bot"
}

# Stop just the python listeners
stop_listen ()
{
  screen -S nasaListener -X quit
  screen -S astroListener -X quit
  echo "Stopped listen"
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Script Arguments:
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if [ ! -n "$1" ]
then
  stop_all
else
  if [ $1 = "all" ] 
  then
    stop_all
  fi
  if [ $1 = "listen" ] 
  then
    stop_listen
  fi
  if [ $1 = "bot" ] 
  then
    stop_bot
  fi
fi
