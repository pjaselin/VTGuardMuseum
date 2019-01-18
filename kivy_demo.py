#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__status__ = "Development"

# necessary library imports
import os
#os.environ['KIVY_BCM_DISPMANX_ID'] = '3' # tells Kivy which display to work with (may need to be changed for tablet interface)
import RPi.GPIO as GPIO
import time
import pigpio
import subprocess
import pygame
from math import copysign
import random
import threading
import multiprocessing
import sys
import threading
import traceback

# kivy library imports
from kivy.app import App
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty
from kivy.core.text import Label as CoreLabel
from kivy.event import EventDispatcher
from kivy.uix.slider import Slider

# start pigpio daemon
subprocess.call("sudo pigpiod &", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# define GPIO pins as variables for readability        
GPIO_LASER = 27
GPIO_SERVOPIN_X = 17 # 540 (right)-2300 (left)
GPIO_SERVOPIN_Y = 4 #550-1750
GPIO_START_BUTTON = 13
servo_step_length = 5
servo_pause = 0.01

# GPIO setup
GPIO.setmode(GPIO.BCM) # set pin numbering
GPIO.setup(GPIO_LASER, GPIO.OUT) # laser control setup
GPIO.setup(GPIO_START_BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_UP) # play button setup

# start pygame to play audio files
pygame.init()

# initialize audio file
audio = pygame.mixer.Sound("/home/pi/Patrick/jfk.wav")

# start pigpio instance 
servo = pigpio.pi()

# define and set initial orientation
initial_x = 1050
initial_y = 800
current_x = initial_x
current_y = initial_y
servo.set_servo_pulsewidth(GPIO_SERVOPIN_X, current_x)
servo.set_servo_pulsewidth(GPIO_SERVOPIN_Y, current_y)

# zero servos
time.sleep(0.1)
servo.set_servo_pulsewidth(GPIO_SERVOPIN_X, 0)
servo.set_servo_pulsewidth(GPIO_SERVOPIN_Y, 0)

def servo_stepper(TARGET_X, TARGET_Y):
    '''
    Input:
        TARGET_X: target pulsewidth x-axis
        TARGET_Y: target pulsewidth y-axis
    Output:
        Limits the servo movement to maximum increments of 50 from current
        location to target x,y location. This serves to quiet the noise
        produced by servo movement.
    '''
    # copy of current coordinates
    position_x = current_x
    position_y = current_y
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
    
    # zero pwm's
    servo.set_servo_pulsewidth(GPIO_SERVOPIN_X, 0)
    servo.set_servo_pulsewidth(GPIO_SERVOPIN_Y, 0)
    
    # return new positions
    return position_x, position_y

def servo_stepper2(START_X, START_Y, TARGET_X, TARGET_Y):
    '''
    Input:
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
    
    # zero pwm's
    servo.set_servo_pulsewidth(GPIO_SERVOPIN_X, 0)
    servo.set_servo_pulsewidth(GPIO_SERVOPIN_Y, 0)
    
    # return new positions
    return position_x, position_y

def thread_demo():
    '''
    Function to run the threading demo
    '''
    count = 0
    while count < 40:
        new_x = random.randint(600, 1400)
        new_y = random.randint(550,900)
        
        coinflip = random.randint(0,2)
        if coinflip == 1:
            GPIO.output(GPIO_LASER, 1)
        
        current_x, current_y = servo_stepper(new_x, new_y)
                
        # turn on/off laser
        GPIO.output(GPIO_LASER, 1)
        time.sleep(random.uniform(3.0,5.0))
        GPIO.output(GPIO_LASER, 0)
                
        # add to counter
        count += 1
        time.sleep(random.randint(2,6))
    current_x, current_y = servo_stepper(initial_x, initial_y)



class RootWidget(FloatLayout):
    X_coord = NumericProperty(initial_x)
    Y_coord = NumericProperty(initial_y)
    #X_next = NumericProperty(0)
    #Y_next = NumericProperty(0)
    
    thread = multiprocessing.Process(target = thread_demo)
    first_run = True
    
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        
        def Full_Demo_callback(instance):
            if not self.first_run:
                self.thread.terminate()
                self.thread = multiprocessing.Process(target = thread_demo)

            audio.stop()
            GPIO.output(GPIO_LASER, 0)
            audio.play()
            
            # sequence for laser and servos
            self.thread.start()
            self.first_run = False
            
        Full_Demo = Button(text="Full Demo",size_hint=(.2, .2), pos_hint={'center_x': .15, 'center_y': .85},font_size='35sp')
        Full_Demo.bind(on_press=Full_Demo_callback)
        self.add_widget(Full_Demo)
        
        def Stop_Full_Demo_callback(instance):
            if not self.first_run:
                self.thread.terminate()
            audio.stop()
            GPIO.output(GPIO_LASER, 0)
            
            servo.set_servo_pulsewidth(GPIO_SERVOPIN_X, initial_x)
            servo.set_servo_pulsewidth(GPIO_SERVOPIN_Y, initial_y)
            self.X_coord = initial_x
            self.Y_coord = initial_y
            
        Stop_Full_Demo = Button(text="Stop Demo",size_hint=(.2, .2), pos_hint={'center_x': .15, 'center_y': .6},font_size='35sp')
        Stop_Full_Demo.bind(on_press=Stop_Full_Demo_callback)
        self.add_widget(Stop_Full_Demo)
        
        ## Laser On/Off Switch
        self.add_widget(Label(text="Laser Power", size_hint=(.15, .15), pos_hint={'center_x': .4, 'center_y': .92}, font_size='23sp'))
        def callback_heat1(instance, value):
            if value == True:
                # when pressed, turn laser on
                GPIO.output(GPIO_LASER, 1)
            else:
                # when depressed turn laser off
                GPIO.output(GPIO_LASER, 0)
        switch_heat1 = Switch(size_hint=(.15, .15), pos_hint={'center_x': .4, 'center_y': .87})
        switch_heat1.bind(active=callback_heat1)
        self.add_widget(switch_heat1)
        
        slider_x = Slider(min = 540, max = 2300, value = 1100, step = 1,
                          pos_hint={'center_x': .55, 'center_y': .4},
                          size_hint=(.4, .4),
                          value_track=True, value_track_color=[1, 0, 0, 1])        
        slider_y = Slider(min = 550, max = 1750, value = 800, step = 1,
                          orientation = "vertical",
                          pos_hint={'center_x': .85, 'center_y': .4},
                          size_hint=(.5, .5),
                          value_track=True, value_track_color=[1, 0, 0, 1],
                          sensitivity = "handle")
        def update_x(instance, value):
            temp_x, temp_y = servo_stepper2(self.X_coord, self.Y_coord, slider_x.value, slider_y.value)
            self.X_coord = temp_x
            self.Y_coord = temp_y
        slider_x.bind(on_touch_up = update_x)
        self.add_widget(slider_x)
        def update_y(instance, value):
            temp_x, temp_y = servo_stepper2(self.X_coord, self.Y_coord, slider_x.value, slider_y.value)
            self.X_coord = temp_x
            self.Y_coord = temp_y
        slider_y.bind(on_touch_up = update_y)
        self.add_widget(slider_y)


class MuralApp(App):
    '''
    Final application assembly into a Kivy App class
    '''
    def build(self):
        self.root = root = RootWidget()
        
        root.bind(size=self._update_rect, pos=self._update_rect)

        with root.canvas.before:
            # RGBA coloring scheme
            #Color(0.851, 0.851, 0.851, 1)
            Color(0.094, 0.141, 0.765, 1)
            self.rect = Rectangle(size=root.size, pos=root.pos)

        return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ == '__main__':
    # if running this file as main:
    
    # start the app
    try:
        MuralApp().run()
        
    except KeyboardInterrupt:
        # stop audio
        audio.stop()
        
        # reset and zero pwm
        current_x, current_y = servo_stepper(initial_x, initial_y)
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
