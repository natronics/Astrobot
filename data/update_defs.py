#!/usr/bin/env python
import util
import json
import datetime

jpl = util.Horizons()

MSL_elements = jpl.get_orbital_elements('-76')
Juno_elements = jpl.get_orbital_elements('-61')

msl = {   "name": "Mars Science Laboratory"
        , "shortcode": "MSL"
        , "description": "A rover currently in route to Mars"
        , "arrival_date": datetime.datetime(2012,8,6,6,15,0).isoformat()
        , "Elements": MSL_elements}
        
juno = {  "name": "Juno"
        , "shortcode": "Juno"
        , "description": "A science mission currently in route to Jupiter"
        , "arrival_date": datetime.datetime(2016,10,19,0,0,0).isoformat()
        , "Elements": Juno_elements}
        
f = open("spacecraft.json", 'w')

f.write(json.dumps({"msl": msl, "juno": juno}))
