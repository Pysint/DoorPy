# DoorPy
Python doorbell application, for use with Raspberry Pi &amp; Display-o-tron 3000.

DoorPy exists of two separated applications:
* webapp.py - For the webapplication;
* doorPy.py - The actual DoorPy application, reading the GPIO input/output and controlls the LCD.

It uses the following applications by design:
* Apache2 (with mod_wsgi enabled);
* Upstart for automated (re)booting of the application.

# Installation
Below a guideline for the installation of DoorPy, it might be incorrect.. Don't blame me for that!

* Fulfil all dependecies:<br/>
`apt-get install apache2 libapache2-mod-wsgi upstart`
* Clone the repository into `/var/www/DoorPy`.
* Install dependecies by using pip:<br/>`pip install -r requirements.txt`
* Setup Apache:
  * Edit `/etc/apach2/sites-enabled/doorpy.conf`, to contain the following:
  ```
  <VirtualHost *:80>
                ServerName [name]
                ServerAdmin [email]

        WSGIDaemonProcess NAME  user=www-data group=www-data threads=5
        WSGIScriptAlias / /var/www/DoorPy/app.wsgi

        <Directory /var/www/DoorPy/app>
                        Order allow,deny
                        Allow from all
                        WSGIScriptReloading On
                </Directory>

        Alias /static /var/www/DoorPy/static
                <Directory /var/www/DoorPy/static/>
                        Order allow,deny
                        Allow from all
                        WSGIScriptReloading On
                </Directory>

        ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
  ```
  * 

