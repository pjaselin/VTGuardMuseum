#!/usr/bin/python
# when this code is called, fully and immediately shutdown the RPi
import subprocess
subprocess.call("sudo shutdown now", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
