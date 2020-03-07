# Installation #

NeoPixel installation instructions from https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/

Install the required packages
```
sudo apt-get install gcc make build-essential python-dev git scons swig
```

Deactivate the audio output for this to work. Edit this file:
```
sudo nano /etc/modprobe.d/snd-blacklist.conf
```
Add the following line:
```
blacklist snd_bcm2835
```

Edit the configuration file:
```
sudo nano /boot/config.txt
```

Comment out the line in the configuration file:
```
# Enable audio (loads snd_bcm2835)
dtparam=audio=on
```
The commented out line should be:
```
# dtparam=audio=on
```

Restart the system:
```
sudo reboot
```

Download the NeoPixel library
```
sudo neopixel_library_install.sh
```


## Launch the server ##
```
sudo python3 sign_server.py
```
