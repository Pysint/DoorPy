#!/usr/bin/python
from datetime import datetime
import RPi.GPIO as GPIO
import time, os, sys 
import sqlite3
import settings as sett
from settings import gpio_bell, logging, debug, timeout, txt_security, txt_pressme, txt_ring, txt_wait, txt_coming, txt_away1, txt_away2, txt_away3

# Set GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_bell, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if logging == "txt":
    logfile = sett.logfile
elif logging == "db":
    conn = sqlite3.connect(sett.database)
    c = conn.cursor()
else:
    sys.exit("[Error] Please choose a proper logging format.")

#############
# FUNCTIONS #
#############

def ts():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

# Logging function will handle all logging requests.
def log(txt):
    if logging == "txt":
        with open(logfile,"a+") as f:
            f.write(ts()+" - "+txt+"\n")
            f.close
    elif logging == "db":
        c.execute("INSERT INTO doorlogs (date, description, note) VALUES (?,'Doorbell rang by someone.','')", (ts(),) )
        conn.commit()
    else:
        sys.exit("Please choose a proper logging format.")
        
# Main function, executed when button is pressed..
def doorbell():
    GPIO.remove_event_detect(gpio_bell) # Ignore multiple clicks

    print(txt_security)                 
    print(txt_ring)
    print ts()
    log("Someone was at your door!")
    if debug:
        z=1
        print("----Debug break "+str(z)+"----") 
    time.sleep(timeout)
    
    print(txt_security)
    print(txt_wait)
    if debug:
        z=z+1
        print("----Debug break "+str(z)+"----") 
    time.sleep(timeout)

# Loop code, on detect run doorbell()-function.
try:
    while True:
        print("\n\n"+txt_pressme)
        GPIO.wait_for_edge(gpio_bell, GPIO.FALLING)
        doorbell()
        time.sleep(sett.sleepaddition)

except KeyboardInterrupt:
    conn.close()
    GPIO.cleanup()

finally:
    conn.close()
    GPIO.cleanup()
