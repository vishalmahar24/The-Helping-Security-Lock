import scipy.io.wavfile as wav
import numpy as np
import buzzer
import speechpy
import os
import pickle
from pydtw import dtw2d
import time

def train(keyid):
    print 'Please speak \'Where are you Lock\' in the mic within 5 seconds of the prompt \'Begin\' !'
    time.sleep(2)
    buzzer.start()
    print 'Begin !'
    os.system('arecord -D sysdefault:CARD=1 -c 1 -f S16 -r 8000 -d 5 /home/pi/snowboytrain.wav')
    #file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)),'train.wav')
    file_name = '/home/pi/snowboytrain.wav'
    fs, signal = wav.read(file_name)
    #signal = signal[:,0]
    keyid=str(keyid)

    ############# Extract MFCC features #############
    mfcc = speechpy.feature.mfcc(signal, sampling_frequency=fs, frame_length=0.020, frame_stride=0.01,
             num_filters=40, fft_length=512, low_frequency=0, high_frequency=None)

    mfccset={}
    if os.path.exists('wheremfccdataset.dat'):
        with open('wheremfccdataset.dat','rb') as readf:
            mfccset=pickle.load(readf)
    mfccset[keyid]=mfcc
    with open('wheremfccdataset.dat','wb') as writef:
        pickle.dump(mfccset,writef,protocol=pickle.HIGHEST_PROTOCOL)
    print 'Please speak \'Open Sesame\' in the mic within 5 seconds of the prompt \'Begin\' !'
    time.sleep(2)
    buzzer.start()
    print 'Begin !'
    os.system('arecord -D sysdefault:CARD=1 -c 1 -f S16 -r 8000 -d 5 /home/pi/snowboytrain.wav')
    #file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)),'train.wav')
    file_name = '/home/pi/snowboytrain.wav'
    fs, signal = wav.read(file_name)
    #signal = signal[:,0]
    keyid=str(keyid)

    ############# Extract MFCC features #############
    mfcc = speechpy.feature.mfcc(signal, sampling_frequency=fs, frame_length=0.020, frame_stride=0.01,
             num_filters=40, fft_length=512, low_frequency=0, high_frequency=None)

    mfccset={}
    if os.path.exists('mfccdataset.dat'):
        with open('mfccdataset.dat','rb') as readf:
            mfccset=pickle.load(readf)
    mfccset[keyid]=mfcc
    with open('mfccdataset.dat','wb') as writef:
        pickle.dump(mfccset,writef,protocol=pickle.HIGHEST_PROTOCOL)
    print 'Successfully added',keyid,'to the database!'



def recog():
    print 'Please speak \'Where are you lock\' or \'Open Sesame\' in the mic within 5 seconds of the prompt \'Begin\' !'
    time.sleep(2)
    buzzer.start()
    print 'Begin !'
    os.system('arecord -D sysdefault:CARD=1 -c 1 -f S16 -r 8000 -d 5 /home/pi/snowboyrecog.wav')
    #file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)),'recog.wav')
    file_name = '/home/pi/snowboyrecog.wav'
    fs, signal = wav.read(file_name)
    #signal = signal[:,0]

    ############# Extract MFCC features #############
    mfcc = speechpy.feature.mfcc(signal, sampling_frequency=fs, frame_length=0.020, frame_stride=0.01,
             num_filters=40, fft_length=512, low_frequency=0, high_frequency=None)
    mfccset={}
    mfccset['unknown']=mfcc
    with open('unknownsample.dat','wb') as writef:
        pickle.dump(mfccset,writef,protocol=pickle.HIGHEST_PROTOCOL)
    mfccsetopen={}
    with open('mfccdataset.dat','rb') as readf:
        mfccsetopen=pickle.load(readf)
    if(len(mfccset)==0):
        return 'No Data'
    mfccdataopen = mfccsetopen.values()
    mfcckeysopen = mfccsetopen.keys()
    n = len(mfccdata)
    with open('unknownsample.dat','rb') as readf:
        aset=pickle.load(readf)
    a=aset.values()[0]
    mindistopen = 10000.000
    minindopen=-1
    for i in range(n):
        b=mfccdataopen[i]
        cost_matrix, alignmend_a, alignmend_b = dtw2d(a, b)
        r,l=cost_matrix.shape
        cost=cost_matrix[r-1][l-1]
        #print "Distance between ",mfcckeys[i]," and given voice is:\t",cost_matrix[r-1][l-1]
        if cost<mindistopen:
            mindistopen=cost
            minindopen=i
    mfccsetwhere={}
    with open('wheremfccdataset.dat','rb') as readf:
        mfccsetwhere=pickle.load(readf)
    mindistwhere = 100000.000
    minindwhere=-1
    mfccdatawhere = mfccsetwhere.values()
    mfcckeyswhere = mfccsetwhere.keys()
    for i in range(n):
        b=mfccdatawhere[i]
        cost_matrix, alignmend_a, alignmend_b = dtw2d(a, b)
        r,l=cost_matrix.shape
        cost=cost_matrix[r-1][l-1]
        #print "Distance between ",mfcckeys[i]," and given voice is:\t",cost_matrix[r-1][l-1]
        if cost<mindistwhere:
            mindistwhere=cost
            minindwhere=i
    if mindistopen>mindistwhere:
        if mindistwhere>=6000 or minindwhere==-1:
            print 'Not Found'
        else:
            return 'Where'
    else:
        if mindistopen>=4000 or minindopen==-1:
            return 'Not Found'
        else:
            return 'Open'
