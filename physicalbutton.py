# -*- coding: utf-8 -*-
__status__ = "Development"
'''
Customer: Vermont National Guard Museum and Library
Description:
    Application that enables side-by-side audio and automated laser pointer presentations
'''

import RPi.GPIO as GPIO
import time
import pigpio
import subprocess
import pygame
from math import copysign
import random
import multiprocessing

# start pigpio daemon
subprocess.call("sudo pigpiod &", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# define GPIO pins as variables for readability
GPIO_LASER = 27
GPIO_SERVOPIN_X = 17 # 540 (right)-2300 (left)
GPIO_SERVOPIN_Y = 4 #550-1750
GPIO_START_BUTTON = 13

# variable for the step length (resolution) taken by servo stepper function
servo_step_length = 5
# variable for pause time between individual steps by servo stepper function
servo_pause = 0.01

# GPIO setup
GPIO.setmode(GPIO.BCM) # set pin numbering
GPIO.setup(GPIO_LASER, GPIO.OUT) # laser control setup
GPIO.setup(GPIO_START_BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_UP) # play button setup

# start pygame to play audio files
pygame.init()
# initialize audio file
audio = pygame.mixer.Sound("/home/pi/museum/jfk.wav")

# start pigpio instance
servo = pigpio.pi()

# define and set initial orientation
initial_x = 1050
initial_y = 800
current_x = initial_x
current_y = initial_y
servo.set_servo_pulsewidth(GPIO_SERVOPIN_X, current_x)
servo.set_servo_pulsewidth(GPIO_SERVOPIN_Y, current_y)
time.sleep(0.1) # brief pause

# turn off servos
servo.set_servo_pulsewidth(GPIO_SERVOPIN_X, 0)
servo.set_servo_pulsewidth(GPIO_SERVOPIN_Y, 0)

def servo_stepper(START_X, START_Y, TARGET_X, TARGET_Y):
    '''
    Input:
        START_X: initial pulsewidth x-axis
        START_Y: initial puslewidth y-axis
        TARGET_X: target pulsewidth x-axis
        TARGET_Y: target pulsewidth y-axis
    Output:
        Limits the servo movement to maximum increments of 50 from current
        location to target x,y location. This serves to quiet the noise
        produced by servo movement.
    '''
    # copy of current coordinates
    position_x = START_X
    position_y = START_Y
    print("target:", TARGET_X, TARGET_Y)
    # get delta between target and current positions
    delta_x = TARGET_X - position_x
    delta_y = TARGET_Y - position_y

    # loop to step from current to target positions
    while abs(delta_x) > servo_step_length or abs(delta_y) > servo_step_length:
        if abs(delta_x) > servo_step_length:
            position_x += copysign(servo_step_length, delta_x) 
            servo.set_servo_pulsewidth(GPIO_SERVOPIN_X, position_x)
            time.sleep(servo_pause)
            servo.set_servo_pulsewidth(GPIO_SERVOPIN_X, 0)
        time.sleep(servo_pause)
        
        if abs(delta_y) > servo_step_length:
            position_y += copysign(servo_step_length, delta_y)
            servo.set_servo_pulsewidth(GPIO_SERVOPIN_Y, position_y)
            time.sleep(servo_pause)
            servo.set_servo_pulsewidth(GPIO_SERVOPIN_Y, 0)
        time.sleep(servo_pause)
        print("temp x:", position_x, "temp y:", position_y)
        
        # update deltas
        delta_x = TARGET_X - position_x
        delta_y = TARGET_Y - position_y
        
        # very brief pause
        time.sleep(servo_pause)
    
    # when close enough, take remainder step
    position_x += delta_x
    position_y += delta_y
    print("new position:", position_x, position_y)
    servo.set_servo_pulsewidth(GPIO_SERVOPIN_X, position_x)
    servo.set_servo_pulsewidth(GPIO_SERVOPIN_Y, position_y)
    time.sleep(servo_pause)
    
    # zero pwm's
    servo.set_servo_pulsewidth(GPIO_SERVOPIN_X, 0)
    servo.set_servo_pulsewidth(GPIO_SERVOPIN_Y, 0)
    
    # return new positions
    return position_x, position_y

def threaded_sequence():
    thread_x = current_x
    thread_y = current_y
    count = 0
    while count < 40:
        new_x = random.randint(600, 1400)
        new_y = random.randint(550,900)
        
        coinflip = random.randint(0,2)
        if coinflip == 1:
            GPIO.output(GPIO_LASER, 1)
        
        thread_x, thread_y = servo_stepper(thread_x, thread_y, new_x, new_y)
                
        # turn on/off laser
        GPIO.output(GPIO_LASER, 1)
        time.sleep(random.uniform(3.0,5.0))
        GPIO.output(GPIO_LASER, 0)
                
        # add to counter
        count += 1
        time.sleep(random.randint(2,6))
    
    # finally return to initial orientation
    thread_x, thread_y = servo_stepper(thread_x,thread_y, initial_x, initial_y)

thread = multiprocessing.Process(target = threaded_sequence)
thread.daemon = True
first_run = True

while True:
    # check button status
    start_button_state = GPIO.input(GPIO_START_BUTTON)
    
    try:
        if start_button_state == True: # capture button press
            # reset audio if necessary
            audio.stop()
            # check that laser is off at start
            GPIO.output(GPIO_LASER, 0)
            
            # start audio
            audio.play()
            
            ## sequence for laser and servos
            # if this is not the first run, kill thread and open new one
            if not first_run:
                thread.terminate()
                #thread.join()
                thread = multiprocessing.Process(target = threaded_sequence)
                thread.daemon = True
            # open thread to run laser/servo sequence
            thread.start()
            #thread.join()
            # set variable to False as this can no longer be the first run
            first_run = False
        
        # pause for next sequence
        time.sleep(0.1)
    
    except KeyboardInterrupt:
        # stop audio
        audio.stop()
        if not first_run:
            thread.terminate()
        
        # reset and zero pwm
        current_x, current_y = servo_stepper(current_x, current_y, initial_x, initial_y)
        time.sleep(0.1)
        servo.set_servo_pulsewidth(GPIO_SERVOPIN_X, 0)
        servo.set_servo_pulsewidth(GPIO_SERVOPIN_Y, 0)
        time.sleep(0.1)
        
        # stop pigpio
        servo.stop()
        
        time.sleep(0.1)
        
        # stop laser if not already
        GPIO.output(GPIO_LASER, 0)
        time.sleep(0.1)
        
        # end GPIO
        GPIO.cleanup()
