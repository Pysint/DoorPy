from datetime import datetime
import RPi.GPIO as GPIO
import time, os, sys 
import sqlite3

# Set GPIO
GPIO.setmode(GPIO.BCM)
gpio_bell = 18     #Doorbell button GPIO pin number
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Text variables, for easy editing of output.
txt_security    = "[Security system online]"
txt_pressme     = "Welcome, please press doorbell."
txt_ring        = "Doorbell is ringing..."
txt_wait        = "Your ring is being processed, hang in there!"
txt_coming      = "I'm on my way!"
txt_away1       = "Sorry, we are currently not at home" 
txt_away2       = "(or we just don't feel like coming downstairs)." 
txt_away3       = "Please deliver packages at out neighbors (no 11)." 

# Logging settings, only SQLite can be used for web interface.
# Choose 'db' or 'txt'.
logging = "txt"
if logging == "txt":
    logfile = "doorbell-log.txt"
elif logging == "db":
    conn = sqlite.connect('doorbell.db')
    c = conn.cursor()
else:
    sys.exit("[Error] Please choose a proper logging format.")

# Other vars;.
debug = True            #Enable/disable debugging
timeout = 1             #Time (seconds) to wait till next message

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
        print("here comes sql cmmds")
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

except KeyboardInterrupt:
    GPIO.cleanup()

finally:
    GPIO.cleanup()
