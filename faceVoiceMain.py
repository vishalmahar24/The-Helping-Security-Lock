def init():
    print 'Please wait initializing system...'

    import sys
    import pickle
    import faceCode
    import voiceCode
    import doorcheck
    import buzzer
    import RPi.GPIO as GPIO
    import time as time
    import servoCode
    import os
    import barFingerMain
    import fingerMain
    import allModulesMain
    import voiceFingerMain
    import barMain
    print 'System initialized! Usage can begin now !'
    time.sleep(2)
    os.system('clear')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    mat = [['1','2','3','A'],
           ['4','5','6','B'],
           ['7','8','9','C'],
           ['*','0','#','D']]

    row = [7,11,13,15]

    col = [12,16,18,32]

    pin = '1234'
    changeModulePin='62018'
    entered = ['0']
    countEntered=0
    switchpin=37
    GPIO.setup(switchpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    for j in range(4):
        GPIO.setup(col[j],GPIO.OUT)
        GPIO.output(col[j],1)

    for i in range(4):
        GPIO.setup(row[i],GPIO.IN,pull_up_down = GPIO.PUD_UP)

    passCorrectFlag=False

    try:
        while(True):
            input_state = GPIO.input(switchpin)
            if input_state == False:
                print '\nOpening Lock!'
                servoCode.turnmotor(-80)
                buzzer.passAccepted()
                doorcheck.checkWhenClosed()
                countEntered=0
            for j in range(4):
                GPIO.output(col[j],0)
                for i in range(4):
                    if GPIO.input(row[i])==0:
                        countEntered+=1
                        if(countEntered>len(entered)):
                            entered.append(mat[i][j])
                        else:
                            entered[countEntered-1]=mat[i][j]
                        if(i==0 and j==3):                  # Key: A
                            #print "Backspace"
                            countEntered-=2
                            os.system('clear')
                        elif(i==3 and j==3):                # Key : D
                            countEntered-=1
                            #print "Enter"
                            p=len(entered)-1
                            while(entered[p]!='D'):
                                del entered[p]
                                p-=1
                            del entered[p]
                            enteredpin = ''.join(entered)
                            if enteredpin==pin:
                                print '\nCorrect Pin!\nOpening Lock!'
                                servoCode.turnmotor(-80)
                                buzzer.passAccepted()
                                doorcheck.checkWhenClosed()
                            elif enteredpin==changeModulePin:
                                print 'Change Module!'
                                time.sleep(0.5)
                                os.system('clear')
                                print 'Please select the module you wish to use:'
                                print '1. Barcode Recognition\t2. Barcode+Finger recognition'
                                print '3. Face+Voice recognition\t4. Voice+Finger recognition'
                                print '5.Finger recognition\t6. All modules together\nChoice:'
                                GPIO.output(col[j],1)
                                numEntered=False
                                while(numEntered==False):
                                    for x in range(4):
                                        GPIO.output(col[x],0)
                                        for z in range(4):
                                            if GPIO.input(row[z])==0:
                                                print z,x
                                                keyentered=mat[z][x]
                                                try:
                                                    ip=int(keyentered)
                                                    if(ip<1 or ip>6):
                                                        print 'Select valid choice!'
                                                    else:
                                                        numEntered=True
                                                        break
                                                except:
                                                    print 'Select valid choice!'
                                        if numEntered==True:
                                            break
                                        GPIO.output(col[x],1)
                                    time.sleep(0.1)
                                GPIO.output(col[j],0)
                                if ip==1:
                                    barMain.init()
                                elif ip==2:
                                    barFingerMain.init()
                                elif ip==3:
                                    print 'It is the current module!\n'
                                elif ip==4:
                                    voiceFingerMain.init()
                                elif ip==5:
                                    fingerMain.init()
                                elif ip==6:
                                    allModulesMain.init()
                                
                            else:
                                print '\nWrong pin!'
                            countEntered=0
                        elif(i==1 and j==3):                # Key : B
                            print "\n Please enter the pin to add user:\n"
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
                                print "\nInitializing User Adding protocol..."
                                print "\nPlease enter numeric id number you wish to give for user"
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
                                print 'Initializing Face addition to database...'
                                faceCode.train(keyid)
                                print 'Face added to database, moving to voice enrollment...'
                                time.sleep(2)
                                voiceCode.train(keyid)
                            else:
                                print 'User not authorized!'
                            countEntered=0
                        elif(i==2 and j==3):                # Key : C
                            #print "Remove User"
                            print "\n Please enter the pin to remove user:\n"
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
                                print "\nInitializing User Deleting protocol..."
                                print "\nPlease enter numeric id number you wish to delete:"
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
                                print'Initializing face deletion...'
                                time.sleep(1)
                                result=faceCode.delete(keyid)
                                if result=='Key Not Present':
                                    print 'Invalid Key Entered!'
                                else:
                                    print'Initializing voice deletion...'
                                    time.sleep(1)
                                    result=voiceCode.delete(keyid)
                                    if result=='Key Not Present':
                                        print 'Invalid Key Entered'
                                countEntered=0
                            else:
                                print 'User not authorized!'
                            countEntered=0
                        elif(i==3 and j==0):                # Key : *
                            #print "Recognise"
                            print 'Initializing face recognition...'
                            result1=faceCode.recog()
                            if result1=='No Data':
                                print 'No data for recognition!'
                            elif result1=='Not Found':
                                print 'Face not recognised!'
                                buzzer.passRejected()
                            else:
                                print 'Face Recognised. Initialising Voice recognition!'
                                time.sleep(2)
                                result2=voiceCode.recog()
                                while(result2=='Not Accurate'):
                                    print 'Not Very Accurate! Please try again!'
                                    result2=voiceCode.recog()
                                if result2=='No Data':
                                    print 'No data for recognition!'
                                elif result2=='Not Found':
                                    print 'Voice not recognised!'
                                    buzzer.passRejected()
                                else:
                                    if result1 == result2:
                                        print 'Opening lock for id key:%s'%(result1)
                                        servoCode.turnmotor(-80)
                                        buzzer.passAccepted()
                                        doorcheck.checkWhenClosed()
                                    else:
                                        print 'Recognised users for Face and Voice Recognition do not match !'
                        elif(i==3 and j==2):                # Key : #
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
                        else:
                            os.system('clear')
                        p=0
                        for p in range(countEntered):
                            print entered[p],
                        print ''
                        while (GPIO.input(row[i])==0):
                            pass
                GPIO.output(col[j],1)
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        GPIO.cleanup()
