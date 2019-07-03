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