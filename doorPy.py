#!/usr/bin/python
import RPi.GPIO as GPIO
import time, os, sys 
import sqlite3
import settings as sett
import dot3k.lcd as lcd
import dot3k.backlight as backlight

from datetime import datetime
from settings import rgb_rbg, timeformat, gpio_bell, logging, debug, timeout, txt_security,\
txt_pressme, txt_ring, txt_ring2, txt_wait1, txt_wait2, txt_wait3, txt_coming,\
txt_away1, txt_away2, txt_away3, txt_package1, txt_package2, txt_package3

# Set GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_bell, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if rgb_rbg:
    backlight.use_rbg()

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
    return datetime.now().strftime(timeformat)

# Logging function will handle all logging requests.
def log(txt):
    if logging == "txt":
        with open(logfile,"a+") as f:
            f.write(ts()+" - "+txt+"\n")
            f.close
    elif logging == "db":
        c.execute("INSERT INTO doorlogs (date, description, note) VALUES (?,?,'')", (ts(),txt,) )
        conn.commit()
    else:
        sys.exit("Please choose a proper logging format.")

def wait_loop(span):
    for i in range(span):
        backlight.set_graph(i/float(span))
        time.sleep(0.05)

# Main functionis,  when idle and when button is pressed..
def idle():
    if debug: print "Start idle function." 
    backlight.off()
    lcd.set_cursor_position(0,0)
    lcd.write(txt_security)
    lcd.set_cursor_position(4,1)
    t = datetime.now().strftime("%H:%M:%S")
    lcd.write(t)
    lcd.set_cursor_position(0,2)
    lcd.write(txt_pressme)
    time.sleep(0.5)
    if debug: print "End idle function.\n"

def doorbell():
    GPIO.remove_event_detect(gpio_bell) # Ignore multiple clicks
    if debug: print("Start of Doorbell function\n") 
    
    # Log the event in the databse
    if debug: print "Doorbell rang at "+ts() 
    log("Someone was at your door!")
    if debug: print "Event logged" 
    
    # ####### #
    # Phase 1 # Ringing.
    # ####### #
    
    # Clear LCD and adjust information
    lcd.clear()
    backlight.rgb(0,0,255)
    lcd.set_cursor_position(0,0)
    lcd.write(txt_security)
    lcd.set_cursor_position(4,1)
    lcd.write(txt_ring)
    lcd.set_cursor_position(1,2)
    lcd.write(txt_ring2)
    if debug: print("Text changed, entering wait_loop*2") 
    wait_loop(300)
    if debug: print("Wait loop done") 
    if debug: print("<< Next Phase >>\n") 
    backlight.set_graph(0)
    
    # ####### #
    # Phase 2 # Trying to contact them.
    # ####### #

    # Clear LCD and adjust information
    lcd.clear()
    backlight.rgb(255,153,0)
    lcd.set_cursor_position(0,0)
    lcd.write(txt_wait1)
    lcd.set_cursor_position(0,1)
    lcd.write(txt_wait2)
    lcd.set_cursor_position(0,2)
    lcd.write(txt_wait3)
    if debug: print("Text changed, entering wait_loop*2") 
    wait_loop(100)
    if debug: print("Wait loop done") 
    if debug: print("<< Next Phase >>\n") 
    backlight.set_graph(0)
    
    # ####### #
    # Phase 3 # No one is there.
    # ####### #

    # Clear LCD and adjust information
    lcd.clear()
    backlight.rgb(255,0,0)
    lcd.set_cursor_position(2,0)
    lcd.write(txt_away1)
    lcd.set_cursor_position(1,1)
    lcd.write(txt_away2)
    lcd.set_cursor_position(0,2)
    lcd.write(txt_away3)
    if debug: print("Text changed, entering wait_loop") 
    wait_loop(80)
    if debug: print("<< Next Phase >>\n") 
    backlight.set_graph(0)
    
    # ####### #
    # Phase 4 # Delivery to the neighbors.
    # ####### #

    # Clear LCD and adjust information
    lcd.clear()
    backlight.rgb(0,255,0)
    lcd.set_cursor_position(1,0)
    lcd.write(txt_package1)
    lcd.set_cursor_position(0,1)
    lcd.write(txt_package2)
    lcd.set_cursor_position(0,2)
    lcd.write(txt_package3)
    if debug: print("Text changed, entering sleep") 
    wait_loop(150)
    if debug: print("Wait loop done") 
    if debug: print("<< End of last Phase >>\n") 
    backlight.set_graph(0)
    lcd.clear()

    if debug: print("End of Doorbell function\n") 
    GPIO.add_event_detect(gpio_bell,GPIO.FALLING)

# First run only; set an even detection on the channel to detect button presses
GPIO.add_event_detect(gpio_bell,GPIO.FALLING)

# Loop code, on detect run doorbell()-function.
try:
    lcd.clear()
    if debug: print("----Start loop----") 
    while True:
        idle()
        if GPIO.event_detected(gpio_bell):
            doorbell()

except KeyboardInterrupt:
    lcd.clear()
    backlight.off()
    conn.close()
    GPIO.cleanup()

finally:
    lcd.clear()
    backlight.off()
    conn.close()
    GPIO.cleanup()
