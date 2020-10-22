import RPi.GPIO as io
import servoCode

def checkWhenClosed():
    io.setwarnings(False)

    io.setmode(io.BOARD)

    ## enter the number of whatever GPIO pin you're using
    door_pin = 29

    ## use the built-in pull-up resistor
    io.setup(door_pin, io.IN, io.PUD_UP)  # activate input with PullUp

    ## initialize as closed 
    door_closed=True
    while door_closed==True:
        if io.input(door_pin)==False:
            print "Door Opened"
            door_closed=False

    ## this loop will execute the if statement that is true
    while door_closed==False:
        if io.input(door_pin)==True:
            print "Door Closed"  # stream a message saying "Close"
            servoCode.turnmotor(50)
            door_closed=True
    #io.cleanup()
