# VTGuardMuseum
This repository serves to store and share scripts as we develop interactive displays for the [VT National Guard Museum](http://vt.public.ng.mil/Museum/). Beyond the specific needs of the museum, the code developed here can be easily repurposed for projects where one would like to have an interactive touchscreen app controlling hardware and software on/from a Raspberry Pi. 

![screenshot of app](/markdown/app_screenshot.jpeg)

## Work Product
The primary objective of this project was to develop an interactive display for [The Great War Painting of Sheridan's Ride](https://www.burlingtonfreepress.com/story/news/2016/05/30/camp-johnson-museum-spotlights-military-history/85131380/). Considering the hefty price tag to contract businesses or use turnkey solutions, it was of particular interest to develop a low-cost system. Of course, the Raspberry Pi is an ideal platform for such a project. This is confirmed as the project cost a total of ~$130.

This mixed-media display was developed on a Raspberry Pi to which was connected a [Pan-Tilt HAT](https://www.adafruit.com/product/3353), a [red laser diode](https://www.adafruit.com/product/1054), and an official [Raspberry Pi touchscreen](https://www.amazon.com/Raspberry-Pi-7-Touchscreen-Display/dp/B0153R2A9I). Yes, there are many wires connected to the Pi and yes it still works! Note that the power leads for the two servos had to be soldered together into a single lead, thus sharing one 5V pin. The other 5V pin had to be dedicated to the touchscreen. The laser required one of the 3V pins.

With the hardware connected, an interactive app was written in the Python-Kivy framework that enables museum visitors to select a full or partial presentation of the mural via the touchscreen display (see sample of the app display above). On button press, the app plays an audio file and moves around the laser pointing to features of interest. Note that in this repository and for development, the audio files are samples of [President Franklin D. Roosevelt's Pearl Harbor Speech](https://archive.org/details/FDR_Declares_War_19411208). For the actual installation, the museum scripted and recorded presentations to insert into this app. Also note that the coordinates and corresponding timestamps of where the laser should point are provided as lists in the kivy_museum_app.py file. In the future, it is certainly possible that more advanced and continuous laser movements could be enabled.

## Technical Objectives Achieved
 - An interactive app that controls the Pi
 - Plays audio files
 - Moves the servo HAT
 - Turns on/off the laser
 - Laser/audio sequenced together
 - Current sequence can be terminated and a new one can be started (stop one audio/laser movement and start another)
 - In-app button to shutdown the app and RPi as well if desired (this is achieved by uncommenting `#subprocess.call("sudo shutdown now", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)` near the end of the code)
 - App can be launched at RPi start (needs to be done by adding kivy_museum_app.py to /etc/rc.local, [see here](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/))

## Technologies Involved
 - Kivy (https://kivy.org/#home): framework for developing interactive applications in Python
 - RPi.GPIO: control of Raspberry Pi pins via GPIO for servos and laser
 - pygame: control audio files
 - threading: enables laser/servo to be sequenced to audio files
 - pigpio: control servo movement

## How to Run Kivy App:
 - SSH into RPi via second computer.
 - Create a new directory (not necessary): mkdir development
 - Enter this directory: cd development
 - Clone repository: git clone https://github.com/pjaselin/VTGuardMuseum.git
 - Enter cloned repo: cd VTGuardMuseum
 - Run Kivy app with: python3 kivy_museum_app.py
 - Terminate app with: CTRL+c
### For Raspberry Pi Touchscreen Configuration
Please be sure to also make the edits noted at the bottom of this page to use the RPi touchscreen with this Kivy app:
https://kivy.org/doc/stable/installation/installation-rpi.html
 
## Deployment with Desktop Shortcuts
As noted before, this repository includes a script to run the app and another to shutdown the RPi. For the museum, it is desirable for both of these functions to be run from desktop shortcuts. In order to obtain both of these functionalities, in the repository directory, run:
```bash
chmod +x kivy_museum_app.py
```
and 
```bash
chmod +x rpi_shutdown.py
```
Next, enter the desktop directly. This will likely work:
```bash
cd ~/Desktop
```
### Kivy App Shortcut
Next create a text file with:
```bash
nano presentation_app.desktop
```
and paste the following into the file, editing the filepaths accordingly:
```
[Desktop Entry]
Version=1.0
Name=Presentation
Comment=Shorcut to launch Python-Kivy app
Exec=<path to repo>/VTGuardMuseum/kivy_museum_app.py
Icon=<path to repo>/VTGuardMuseum/markdown/icon.jpg
Path=<path to repo>/VTGuardMuseum
Terminal=false
Type=Application
Categories=Utility;Application;
```
### Shutdown Shortcut
Again create a text file with:
```bash
nano shutdown.desktop
```
and paste the following into the file, editing the filepaths accordingly:
```
[Desktop Entry]
Version=1.0
Name=Shutdown
Comment=Shorcut to shutdown RPi
Exec=<path to repo>/VTGuardMuseum/rpi_shutdown.py
Icon=<path to repo>/VTGuardMuseum/markdown/shutdown_icon.png
Path=<path to repo>/VTGuardMuseum
Terminal=false
Type=Application
Categories=Utility;Application;
```
By now, there should be two shortcuts on the Raspberry Pi desktop with icons, one to launch the app and another to shutdown the RPi.

## Final Notes
Hopefully this is the first of more and similar projects that leverage the Raspberry Pi as an effective and powerful platform for open-source development of museum displays. In the future, I would like to develop a more sophisticated/modern display at the least for my own benefit but also expand the potential for this kind of system.
