# DoorPy
Python doorbell application, for use with Raspberry Pi &amp; Display-o-tron 3000.

DoorPy exists of two separated applications:
* webapp.py - For the webapplication;
* doorPy.py - The actual DoorPy application, reading the GPIO input/output and controlls the LCD.

It uses the following applications by design:
* Apache2 (with modwsgi enabled);
* Upstart for automated (re)booting of the application.

# Installation
* Clone the repository.
* Install dependecies by using pip ('''pip install -r requirements.txt''').
* 

