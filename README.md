# VTGuardMuseum

Repository to store and share development scripts as we develop interactive displays for the VT National Guard Museum: http://vt.public.ng.mil/Museum/.

## Tasks
As this is still in development, there are several key issues that need to be resolved. Chief among these is the desire to be able to terminate a sequence at any time. To achieve this, an audio file needs to be launched and terminated in a thread.

 - thread management via threading.Threading

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
 - Run Kivy app with: python3 kivy_demo.py
 - Terminate app with: CTRL+c
