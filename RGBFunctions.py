import RPi.GPIO as GPIO
import time

red = 16
green = 20
blue = 21

"""
Initialize GPIO pins
"""
def init():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(red, GPIO.OUT)
    GPIO.setup(green, GPIO.OUT)
    GPIO.setup(blue, GPIO.OUT)

    global RED
    global GREEN
    global BLUE

    RED = GPIO.PWM(red, 100)
    GREEN = GPIO.PWM(green, 100)
    BLUE = GPIO.PWM(blue, 100)

    RED.start(0)
    GREEN.start(0)
    BLUE.start(0)

"""
Change LED color to "BUSY" status
"""
def setLEDBusy():
    RED.ChangeDutyCycle(1.0)
    GREEN.ChangeDutyCycle(0)
    BLUE.ChangeDutyCycle(0)

"""
Change LED color to "READY" status
"""
def setLEDReady():
    RED.ChangeDutyCycle(0)
    GREEN.ChangeDutyCycle(1.0)
    BLUE.ChangeDutyCycle(0)

"""
Change LED color to "ACTIVE" status
"""
def setLEDActive():
    RED.ChangeDutyCycle(0)
    GREEN.ChangeDutyCycle(0)
    BLUE.ChangeDutyCycle(1)
    time.sleep(0.5)
    setLEDBusy()

"""
GPIO destructor
"""
def destroy():
    GPIO.cleanup()