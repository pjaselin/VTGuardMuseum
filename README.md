# VTGuardMuseum
This repository primarily serves to store and share scripts as we develop interactive displays for the VT National Guard Museum: http://vt.public.ng.mil/Museum/. 

![screenshot of app](/markdown/app_screenshot.jpeg)

## Work Product
Beyond the specific needs of the museum, the codes created here can be easily repurposed for a multitude of other applications where one would like to build a Kivy app in Python to control hardware and software on/from a Raspberry Pi. Here the app controls a Pan-Tilt HAT (https://www.adafruit.com/product/3353) to which is mounted a red laser diode (https://www.adafruit.com/product/1054). Museum guests control the app through the official Raspberry Pi touchscreen (https://www.amazon.com/Raspberry-Pi-7-Touchscreen-Display/dp/B0153R2A9I). Yes, there are many wires connected to the Pi and yes it still works! Note that the power leads for the two servos had to be soldered together into a single lead, sharing one 5V pin. The other 5V pin had to be dedicated to the touchscreen and the laser required on 3V pin. An astute observer may note this is basically a glorified laser cat toy, but it does the job!

## Specific Objectives Achieved
 - An interactive app that controls the Pi
 - Plays audio files
 - Moves the servo HAT
 - Turns on/off the laser
 - Laser/audio sequenced together
 - Current sequence can be terminated and a new one can be started (stop one audio/laser movement and start another)

## Technologies Involved
 - Kivy (https://kivy.org/#home): framework for developing interactive applications in Python
 - RPi.GPIO: control of Raspberry Pi pins via GPIO for servos and laser
 - pygame: control audio files
 - threading: enables laser/servo to be sequenced to audio files
 - pigpio: control servo movement

## Notes
 - audio files are loaded into memory with pygame, but it might be better to use subprocess calls
 - move servo_stepper to class for easier storage of current position
 - want to make app executable: https://stackoverflow.com/questions/27494758/how-do-i-make-a-python-script-executable
 - possibly also launch at start: https://www.raspberrypi.org/forums/viewtopic.php?t=125129

## How to run Kivy app:
 - SSH into RPi via second computer.
 - Create a new directory: mkdir development
 - Enter this directory: cd development
 - Clone repository: git clone https://github.com/pjaselin/VTGuardMuseum.git
 - Enter cloned repo: cd VTGuardMuseum
 - Run Kivy app with: python3 kivy_museum_app.py
 - Terminate app with: CTRL+c
 
## To do:
 - write instructions to make app executable

## For Raspberry Pi
Please be sure to also make the edits noted at the bottom of this page to use the RPi touchscreen with this Kivy app:
https://kivy.org/doc/stable/installation/installation-rpi.html
