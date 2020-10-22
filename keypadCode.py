import RPi.GPIO as GPIO
import time as time
import servoCode
import doorcheck
import os
GPIO.setmode(GPIO.BOARD)

mat = [['1','2','3','A'],
       ['4','5','6','B'],
       ['7','8','9','C'],
       ['*','0','#','D']]

row = [7,11,13,15]

col = [12,16,18,32]

#pin = ['1','2','3','4']
pin='1234'
entered = ['0','0','0','0']
countEntered=0
countStandBy=0
MaxStandBy=50

for j in range(4):
    GPIO.setup(col[j],GPIO.OUT)
    GPIO.output(col[j],1)

for i in range(4):
    GPIO.setup(row[i],GPIO.IN,pull_up_down = GPIO.PUD_UP)
switchpin=37
GPIO.setup(switchpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
passCorrectFlag=False

try:
    while(True):
        input_state = GPIO.input(switchpin)
        if input_state == False:
            print '\nOpening Lock!'
            servoCode.turnmotor(-80)
            doorcheck.checkWhenClosed()
            countEntered=0
        numEntered=False
        for j in range(4):
            GPIO.output(col[j],0)
            for i in range(4):
                if GPIO.input(row[i])==0:
                    numEntered=True
                    countEntered+=1
                    entered[countEntered-1]=mat[i][j]
                    if(i==0 and j==3):
                        print "Backspace"
                        countEntered=0
                    elif(i==3 and j==3):
                        print "Enter"
                        countEntered=0
                    elif(i==1 and j==3):
                        print "Add User"
                        countEntered=0
                    elif(i==2 and j==3):
                        print "Remove User"
                        countEntered=0
                    elif(i==3 and j==2):
                        print 'You wish to change pin!\n'
                        print 'Please enter the current pin!'
                        time.sleep(1.5)
                        os.system('clear')
                        keyentered='0'
                        countKey=0
                        keyid=[]
                        GPIO.output(col[j],1)
                        time.sleep(0.1)
                        while(keyentered!=mat[3][3] or countKey==0):
                            for q in range(4):
                                GPIO.output(col[q],0)
                                for w in range(4):
                                    if GPIO.input(row[w])==0:
                                        keyentered=mat[w][q]
                                        if(keyentered=='D'):
                                            break
                                        elif(keyentered=='A'):
                                            countKey-=1
                                            os.system('clear')
                                        else:
                                            os.system('clear')
                                            countKey+=1
                                            if(countKey>len(keyid)):
                                                keyid.append(keyentered)
                                            else:
                                                keyid[countKey-1]=keyentered
                                        z=0
                                        for z in range(countKey):
                                            print keyid[z],
                                        print ''
                                    while (GPIO.input(row[w])==0):
                                        pass
                                GPIO.output(col[q],1)
                            time.sleep(0.1)
                        p=len(keyid)-1
                        while(p>=countKey):
                            del keyid[p]
                            p-=1
                        keyid=''.join(keyid)
                        if keyid==pin:
                            print 'Pin verified !\n\nPlease enter the new pin!'
                            time.sleep(1.5)
                            os.system('clear')
                            keyentered='0'
                            countKey=0
                            keyid=[]
                            GPIO.output(col[j],1)
                            time.sleep(0.1)
                            while(keyentered!=mat[3][3] or countKey==0):
                                for q in range(4):
                                    GPIO.output(col[q],0)
                                    for w in range(4):
                                        if GPIO.input(row[w])==0:
                                            keyentered=mat[w][q]
                                            if(keyentered=='D'):
                                                break
                                            elif(keyentered=='A'):
                                                countKey-=1
                                                os.system('clear')
                                            elif(keyentered=='*' or keyentered=='#' or keyentered=='B' or keyentered=='C'):
                                                print 'Please use only numbers!'
                                            else:
                                                os.system('clear')
                                                countKey+=1
                                                if(countKey>len(keyid)):
                                                    keyid.append(keyentered)
                                                else:
                                                    keyid[countKey-1]=keyentered
                                            z=0
                                            for z in range(countKey):
                                                print keyid[z],
                                            print ''
                                        while (GPIO.input(row[w])==0):
                                            pass
                                    GPIO.output(col[q],1)
                                time.sleep(0.1)
                            p=len(keyid)-1
                            while(p>=countKey):
                                del keyid[p]
                                p-=1
                            keyid=''.join(keyid)
                            pin = keyid
                            print 'Pin Changed!'
                        else:
                            print 'Old pin not correct!'
                    print mat[i][j],
                    while (GPIO.input(row[i])==0):
                        pass
            GPIO.output(col[j],1)
        if countEntered==4:
            passCorrectFlag=True
            countEntered=0
            for k in range(4):
                if pin[k]!=entered[k] :
                    passCorrectFlag=False
                    break
            if passCorrectFlag :
                print '\nCorrect Password!'
                servoCode.turnmotor(-80)
                doorcheck.checkWhenClosed()
            else :
                print '\nWrong Password!'
            for k in range(4):
                entered[k]='0'
        if numEntered==True:
            countStandBy=0
        if numEntered==False:
            countStandBy+=1
        if (countStandBy > MaxStandBy and passCorrectFlag==True):
            passCorrectFlag=False
            countStandBy=0
            for k in range(4):
                entered[k]='0'
            #servoCode.initMotor(-50)
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
