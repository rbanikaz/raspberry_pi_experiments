#Jenkins Build Status LED Matrix

TODO: Pic

###Hardware:
* Raspberry Pi 2, Model B
* Edimax N150 Nano Wifi Adapter
* Adafruit RGB Matrix HAT + RTC for Raspberry Pi
* Adafruit 16x32 RGB LED Matrix Panel
* 5V 2A Switching power supply

###Pi Setup
1. Assemble RGB Matrix Hat (some soldering required)
  1. https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/assembly
  2. https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices
2. Setup Raspberry Pi:
  1. Raspberian Jesse Lite:
    1. https://www.raspberrypi.org/downloads/raspbian/
    2. https://www.raspberrypi.org/documentation/installation/installing-images/README.md
  2. Once the OS is flashed, plug the pi into the hdmi monitor and login to the bash shell (pi / raspberry)
    1. SSH: https://www.raspberrypi.org/documentation/remote-access/ssh/
    2. WIFI: https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md
  3. You should be able to login to the pi and connect to the internet (`curl -I google.com`)
3. Login to the pi and install and run demo software
  1. Step 6: https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices 
4. SCP files from this directory into the `rpi-` directory
  1. Create an auth.json file with your jenkins login info   
  
    
