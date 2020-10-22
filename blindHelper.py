import sys
sys.path.append('/home/pi/DPCodes/SpeechRecog/snowboy/snowboy/examples/Python/')
sys.path.append('/home/pi/DPCodes')
import snowboydecoder
import sys
import signal
import buzzer
import mfcctest
import doorcheck
import fingerCode
interrupted=False
def detected_word():
        buzzer.start()
        result=mfcctest.recog()
        if result==
        print 'Initializing fingerprint recognition...'
                            time.sleep(1)
                            result=fingerCode.search()
                            while(result=='Not Accurate'):
                                print 'Not Very Accurate! Please try again!'
                                result=fingerCode.search()
                            if result=='Sensor Error':
                                print 'The Sensor is not working properly. Please contact the service personnel. Sorry for the inconvinience!'
                            elif result=='Unknown Error':
                                print 'Some unknown error occured. Please contact the service personnel. Sorry for the inconvinience!'
                            elif result=='Not Found':
                                print 'Fingerprint not recognised!'        
                            else:
                                print 'Opening lock for id key:%s'%(result)
                                servoCode.turnmotor(40)
                                doorcheck.checkWhenClosed()
def signal_handler(signal, frame):
    global interrupted
    interrupted = True
def interrupt_callback():
    global interrupted
    return interrupted
def detectword():
    model = '/home/pi/DPCodes/SpeechRecog/snowboy/snowboy/examples/Python/snowboy.umdl'
    signal.signal(signal.SIGINT, signal_handler)
    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.8)
    print('Listening... Press Ctrl+C to exit')
    # main loop
    detector.start(detected_callback=detected_word,interrupt_check=interrupt_callback,sleep_time=0.03)
    detector.terminate()

detectword()
