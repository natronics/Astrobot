#INSTALL

The IRC is handled by NodeJS and the astronomical calcualtion is done in python

Some packages that might be useful:

### Base Languages

    $ sudo apt-get install python nodejs redis-server

### Python Redis bindings

    $ sudo apt-get install python-redis

### Python Astronomical library

http://rhodesmill.org/pyephem/

Python 2.x

    $ sudo easy_install pyephem

Python 3

    $ sudo easy_install ephem

### Redis and IRC node bindings via npm

http://npmjs.org/

    $ npm install redis irc

## Config:

Edit config.js.dist with the names and channels that you want the rename to config.js

## Run:

Once config.js is in place run with

    $ ./start.sh
