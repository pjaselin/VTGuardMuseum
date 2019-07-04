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
    #print("target:", TARGET_X, TARGET_Y)
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
        #print("temp x:", position_x, "temp y:", position_y)
        
        # update deltas
        delta_x = TARGET_X - position_x
        delta_y = TARGET_Y - position_y
        
        # very brief pause
        time.sleep(servo_pause)
    
    # when close enough, take remainder step
    position_x += delta_x
    position_y += delta_y
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
    #print("target:", TARGET_X, TARGET_Y)
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
        #print("temp x:", position_x, "temp y:", position_y)
        
        # update deltas
        delta_x = TARGET_X - position_x
        delta_y = TARGET_Y - position_y
        
        # very brief pause
        time.sleep(servo_pause)
    
    # when close enough, take remainder step
    position_x += delta_x
    position_y += delta_y
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
    
    
class StoppableThread(threading.Thread):
    def __init(self)__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()
    
    def stop(self):
        self._stop_event.set()
    
    def stopped(self):
        return self._stop_event.is_set()
    
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