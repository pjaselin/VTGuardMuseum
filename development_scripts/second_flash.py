import time

import pigpio

pi = pigpio.pi() # Connect to local Pi.
time.sleep(1)

while True:
    try:
        pi.set_servo_pulsewidth(4, 600)
        time.sleep(1)
        pi.set_servo_pulsewidth(4, 900)
        time.sleep(1)
        pi.set_servo_pulsewidth(4, 1200)
        time.sleep(1)
        pi.set_servo_pulsewidth(4, 900)
        time.sleep(1)
    
    except KeyboardInterrupt:
        # switch servo off
        pi.set_servo_pulsewidth(17, 0)
        pi.stop()
