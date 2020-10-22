import time
from pyfingerprint.pyfingerprint import PyFingerprint
import os
import pickle

def enroll(keyid):
    ## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        return 'Sensor Error'

    ## Gets some sensor information
    #print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
    fingerdata={}
    if os.path.exists('dataset_fingers.dat'):
        with open('dataset_fingers.dat','rb') as rf:
            fingerdata = pickle.load(rf)
    ## Tries to enroll new finger
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            print('Finger already present!')
            return 2

        print('Remove finger...')
        time.sleep(1)

        print('Waiting for same finger again...')

        ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(0x02)

        ## Compares the charbuffers
        if ( f.compareCharacteristics() == 0 ):
            raise Exception('Fingers do not match')

        ## Creates a template
        f.createTemplate()

        ## Saves template at new position number
        positionNumber = f.storeTemplate()
        fingerdata[str(positionNumber)]=str(keyid)
        with open('dataset_fingers.dat','wb') as wf:
            pickle.dump(fingerdata,wf)
        print 'Finger enrolled successfully for '+str(keyid)+' !'
        #print('New template position #' + str(positionNumber))
        return 'Successful'

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        return 'Unknown Error'


def delete(keyid):
    ## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        return 'Sensor Error'

    ## Gets some sensor information
    #print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    ## Tries to delete the template of the finger
    try:
        keyid=str(keyid)
        fingerset={}
        if os.path.exists('dataset_fingers.dat'):
            with open('dataset_fingers.dat','rb') as readf:
                fingerset=pickle.load(readf)
        keys = fingerset.keys()
        values = fingerset.values()
        hasFlag=False
        posNo=-1
        for i in range(len(keys)):
            if values[i]==keyid:
                hasFlag=True
                posNo = int(keys[i])
                break
        if hasFlag==False:
            return 'Key Not Present'
        del fingerset[str(posNo)]
        with open('dataset_fingers.dat','wb') as writef:
            pickle.dump(fingerset,writef,protocol=pickle.HIGHEST_PROTOCOL)
        if ( f.deleteTemplate(posNo) == True ):
            print 'Successfully deleted',keyid,'from the database!'
            return 'Done'

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        return 'Unknown Error'


def search():

    ## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        return 'Sensor Error'

    ## Gets some sensor information
    #print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
    fingerdata={}
    if os.path.exists('dataset_fingers.dat'):
        with open('dataset_fingers.dat','rb') as rf:
            fingerdata = pickle.load(rf)
    if len(fingerdata)==0:
        return 'No Data'
    ## Tries to search the finger and calculate hash
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Searchs template
        result = f.searchTemplate()

        positionNumber = result[0]
        print positionNumber
        accuracyScore = result[1]
        if ( positionNumber == -1 ):
            return 'Not Found'
        elif (accuracyScore<150):
            return 'Not Accurate'
        else:
            print "Fingerprint recognized!"
            return fingerdata[str(positionNumber)]
        
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        return 'Sensor Error'
