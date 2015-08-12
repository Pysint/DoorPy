#!/usr/bin/python
activate_this = '/home/pi/DoorPy/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/pi/DoorPy/")

from webapp import app as application
application.secret_key = 'Diplay-o-tron3000,raspi,more.raspi'
