import RPi.GPIO as GPIO
import time
 
GPIO_LASER = 27
 
if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_LASER, GPIO.OUT)
 
    print('blinking laser...')
    while True:
        try:  
        # Test turning the laser on and off
            time.sleep(.3)
            GPIO.output(GPIO_LASER, 1)
            time.sleep(.3)
            GPIO.output(GPIO_LASER, 0)
            time.sleep(.3)
            GPIO.output(GPIO_LASER, 1)
            time.sleep(.3)
            GPIO.output(GPIO_LASER, 0)
        except KeyboardInterrupt:
            GPIO.output(GPIO_LASER, 0)
            GPIO.cleanup()
