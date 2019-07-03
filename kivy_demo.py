#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__status__ = "Development"

# necessary library imports
import os, sys
os.environ['KIVY_GL_BACKEND'] = 'gl'
#os.environ['KIVY_BCM_DISPMANX_ID'] = '3' # tells Kivy which display to work with (may need to be changed for tablet interface)
import RPi.GPIO as GPIO
import time, random
import pigpio
import subprocess, threading, multiprocessing
import pygame, pigpio
from math import copysign
import traceback
#from datetime import datetime
import threading
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
#GPIO.setup(GPIO_START_BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_UP) # play button setup

# start pygame to play audio files
pygame.init()

# initialize audio files
full_audio = pygame.mixer.Sound("./audiofiles/fdr_full.wav")
sample0 = pygame.mixer.Sound("./audiofiles/sample_0.wav")
sample1 = pygame.mixer.Sound("./audiofiles/sample_1.wav")
sample2 = pygame.mixer.Sound("./audiofiles/sample_2.wav")
sample3 = pygame.mixer.Sound("./audiofiles/sample_3.wav")
sample4 = pygame.mixer.Sound("./audiofiles/sample_4.wav")

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

###########################  
## Define time sequences and coordinates
# Main Presentation
coordinates_main = [(969, 572), (793, 742), (1071, 700), (687, 573), (692, 892), (989, 551), (719, 880), (951, 754), (1181, 640), (929, 649), (854, 724), (603, 592), (804, 777), (815, 698), (652, 632), (804, 883), (627, 585), (932, 879), (627, 736), (1121, 711)]
timestamps_main = [15, 29, 41, 56, 66, 76, 90, 104, 114, 125, 139, 154, 164, 176, 186, 201, 216, 226, 241, 252]

# Option 1
coordinates_option1 = [(862, 584), (1340, 799), (939, 596), (878, 792), (864, 570), (966, 894), (1350, 831), (860, 690), (1297, 640), (971, 833), (1298, 885), (883, 678), (1298, 894), (871, 853), (694, 846), (1004, 703), (834, 876), (1393, 669), (993, 719), (1114, 886)]
timestamps_option1 = [13, 23, 36, 51, 63, 75, 90, 105, 118, 133, 143, 155, 169, 184, 196, 208, 221, 235, 248, 263]

# Option 2
coordinates_option2 = [(1231, 870), (814, 761), (1177, 659), (673, 710), (834, 640), (900, 625), (1388, 895), (1353, 738), (765, 577), (1216, 778), (611, 852), (770, 606), (1189, 721), (688, 900), (927, 702), (902, 706), (730, 670), (842, 725), (759, 815), (629, 711)]
timestamps_option2 = [10, 20, 30, 41, 56, 66, 80, 90, 105, 116, 129, 140, 154, 169, 182, 197, 210, 224, 236, 249]

# Option 3
coordinates_option3 = [(853, 758), (607, 750), (704, 693), (1269, 592), (1136, 743), (1281, 839), (1042, 631), (1243, 667), (1186, 645), (866, 740), (1338, 765), (751, 664), (1066, 760), (1145, 582), (726, 896), (935, 816), (939, 851), (1136, 674), (1280, 550), (776, 895)]
timestamps_option3 = [13, 24, 36, 51, 65, 75, 87, 102, 115, 130, 142, 154, 169, 183, 193, 208, 222, 232, 244, 255]
###########################



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

class StoppableThread(threading.Thread):
    def __init(self)__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()
    
    def stop(self):
        self._stop_event.set()
    
    def stopped(self):
        return self._stop_event.is_set()


class RootWidget(FloatLayout):
    X_coord = NumericProperty(initial_x)
    Y_coord = NumericProperty(initial_y)
    #X_next = NumericProperty(0)
    #Y_next = NumericProperty(0)
    
    thread = multiprocessing.Process(target = thread_demo)
    first_run = True
    stop_playing = True
    
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        def main_presentation_callback(instance):
            if not self.first_run:
                self.thread.terminate()
                self.thread = multiprocessing.Process(target = thread_demo)
            full_audio.stop()
            GPIO.output(GPIO_LASER, 0)
            full_audio.play()
            
            # sequence for laser and servos
            self.thread.start()
            self.first_run = False
        
        def servo_stepper(self, TARGET_X, TARGET_Y):
            '''
            Input:
                TARGET_X: target pulsewidth x-axis
                TARGET_Y: target pulsewidth y-axis
            Output:
                Limits the servo movement to maximum increments of 50 from current
                location to target x,y location. This is to reduce the noise
                produced by servo movement.
            '''
            # copy of current coordinates
            #position_x = current_x
            #position_y = current_y
            #print("target:", TARGET_X, TARGET_Y)
            # get delta between target and current positions
            delta_x = TARGET_X - self.X_coord
            delta_y = TARGET_Y - self.Y_coord

            # loop to step from current to target positions
            while abs(delta_x) > servo_step_length or abs(delta_y) > servo_step_length:
                if abs(delta_x) > servo_step_length:
                    self.X_coord += copysign(servo_step_length, delta_x)
                    servo.set_servo_pulsewidth(GPIO_SERVOPIN_X, self.X_coord)
                    time.sleep(servo_pause)
                    servo.set_servo_pulsewidth(GPIO_SERVOPIN_X, 0)
                    time.sleep(servo_pause)

                if abs(delta_y) > servo_step_length:
                    self.Y_coord += copysign(servo_step_length, delta_y)
                    servo.set_servo_pulsewidth(GPIO_SERVOPIN_Y, self.Y_coord)
                    time.sleep(servo_pause)
                    servo.set_servo_pulsewidth(GPIO_SERVOPIN_Y, 0)
                    time.sleep(servo_pause)
                #print("temp x:", position_x, "temp y:", position_y)
        
                # update deltas
                delta_x = TARGET_X - self.X_coord
                delta_y = TARGET_Y - self.Y_coord
        
                # very brief pause
                time.sleep(servo_pause)
    
            # when close enough, take remainder step
            self.X_coord += delta_x
            self.Y_coord += delta_y
            servo.set_servo_pulsewidth(GPIO_SERVOPIN_X, self.X_coord)
            servo.set_servo_pulsewidth(GPIO_SERVOPIN_Y, self.Y_coord)
    
            # zero pwm's
            servo.set_servo_pulsewidth(GPIO_SERVOPIN_X, 0)
            servo.set_servo_pulsewidth(GPIO_SERVOPIN_Y, 0)
    
            # return new positions
            #return position_x, position_y
        def example_callback(self, input_coords, input_timestamps):
            # loop through coords at timestamps
            first_timestamp = time.time()
            for i_coords in range(len(input_coords)):
                while first_timestamp - int(time.time()) < input_timestamps[i]:
                    # wait until we reach the target time
                    time.sleep(0.1)
                # then move the laser
                servo_stepper(input_coords[i][0], input_coords[i][1])
        
        def example_callback
                
        
        main_presentation = Button(text="Main\nPresentation", halign='center', size_hint=(.35, .85), pos_hint={'center_x': .25, 'center_y': .5},font_size='25sp')
        main_presentation.bind(on_press=main_presentation_callback)
        self.add_widget(main_presentation)

        option1 = Button(text="Option 1",size_hint=(.25, .25), pos_hint={'center_x': .7, 'center_y': .8},font_size='25sp')
        #option1.bind(on_press=option1_callback)
        self.add_widget(option1)

        option2 = Button(text="Option 2",size_hint=(.25, .25), pos_hint={'center_x': .7, 'center_y': .5},font_size='25sp')
        #option2.bind(on_press=option2_callback)
        self.add_widget(option2)
       
        option3 = Button(text="Option 3",size_hint=(.25, .25), pos_hint={'center_x': .7, 'center_y': .2},font_size='25sp')
        #option3.bind(on_press=option3_callback)
        self.add_widget(option3)

        '''
        def Stop_Full_Demo_callback(instance):
            if not self.first_run:
                self.thread.terminate()
            full_audio.stop()
            GPIO.output(GPIO_LASER, 0)
            
            servo.set_servo_pulsewidth(GPIO_SERVOPIN_X, initial_x)
            servo.set_servo_pulsewidth(GPIO_SERVOPIN_Y, initial_y)
            self.X_coord = initial_x
            self.Y_coord = initial_y
            
        Stop_Full_Demo = Button(text="Stop Demo",size_hint=(.2, .2), pos_hint={'center_x': .15, 'center_y': .6},font_size='25sp')
        Stop_Full_Demo.bind(on_press=Stop_Full_Demo_callback)
        self.add_widget(Stop_Full_Demo)
        
        
        # add segments below
        
        def OffSwitch_callback(instance):
            App.get_running_app().stop()
        OffSwitch = Button(text="Off",size_hint=(.2, .2), pos_hint={'center_x': .15, 'center_y': .35},font_size='25sp')
        OffSwitch.bind(on_press=OffSwitch_callback)
        self.add_widget(OffSwitch)
        '''

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
            Color(140/255, 150/255, 150/255, 1)
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
        full_audio.stop()
        
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
