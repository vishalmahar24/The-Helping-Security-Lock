import RPi.GPIO as GPIO
from time import sleep

def turnmotor(angle):
    gpiopin=33
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(gpiopin,GPIO.OUT)
    pwm=GPIO.PWM(gpiopin,50)
    pwm.start(0)
    if angle<0:
        duty=angle/18+22
        angle=angle*-1
    else:
        duty=angle/18 + 2
    GPIO.output(gpiopin,True)
    pwm.ChangeDutyCycle(duty)
    reqTime=0.275*angle/60
    #sleep(5)
    sleep(reqTime)
    GPIO.output(gpiopin,False)
    pwm.ChangeDutyCycle(0)
    pwm.stop()
