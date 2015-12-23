#
# Settings configuration file.
# In this file all settings for this project can be set.
# Afftected files: webapp.py, doorPy.py

#########################
### Project settings  ###
#########################

# Debug, set to false before going live.
debug =  True

################################
### Web Application Settings ###
################################

# General Webapp configuration
secretkey = '[supersecretkey]
database = '/var/www/DoorPy/doorPy.db'

# Global variables used in the application
name = "DoorPy"
slogan = "A remote doorbell application for Raspberry Pi!"

#######################
### DoorPy Settings ###
#######################

# Enable to swap RGB with RBG colour codes.
# Only needed if you have an early DoT3K.
rgb_rbg = True

# Set GPIO
gpio_bell = 21 #Doorbell button GPIO name (NOT pin#)

# Logging settings, only SQLite can be used for web interface.
# Choose 'db' or 'txt'.
logging = "db"
logfile = "doorbell-log.txt" #Only needed if logging == txt

# Change the format of timestamps
timeformat = "%a %d %b - %H:%M:%S"
# For example:
# "%c" (Same to set locale)
#"%d-%M-%Y %H:%M:%S" (21-12-2000 23:12:59)

# Pushover can be used to send messages.
# If you enable it, make sure to alter variables below.
push_enabled = True
push_app_key = "[yourpusoverhappkey]"
push_user_key = "[yourpushoveruserkey]"

# Enable taking pictures with webcam?
# Highly experimental though, using an IP camera stream embedded on the front-page.
pictures_enabled = False
snap_url = '[snip]' 
stream_url = '[snip]/videostream.cgi' 
outputpath = "static/camera-output/"

# Text variables, for easy editing of output.
# This text will display on the DoT3k
# Take note of the hashtags indicating the end of line. Dont go over it, or will look funky!
txt_security    = "[System online] "#
txt_pressme     = " "               #
txt_ring        = "Contacting...   "#
txt_ring2       = "Please wait! :) "#
txt_wait1       = "Hang on,        "#
txt_wait2       = "Trying to       "#
txt_wait3       = "contact again!  "#
txt_away1       = "Sorry, none is  "#
txt_away2       = "available right "#
txt_away3       = "now or busy!    "#
txt_package1    = "Got a delivery? "#
txt_package2    = "Please deliver  "#
txt_package3    = "another day!    "#
txt_coming      = "I'm on my way!  "#
