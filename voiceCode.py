import scipy.io.wavfile as wav
import numpy as np
import speechpy
import os
import pickle
from pydtw import dtw2d
import time

def train(keyid):
    print 'Please speak \'Open Sesame\' in the mic within 3 seconds of the prompt \'Begin\' !'
    time.sleep(2)
    print 'Begin !'
    os.system('arecord -D sysdefault:CARD=1 -c 1 -f S16 -r 8000 -d 3 /home/pi/DPCodes/Modules/train.wav')
    #file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)),'train.wav')
    file_name = '/home/pi/DPCodes/Modules/train.wav'
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
    print 'Please speak \'Open Sesame\' in the mic within 3 seconds of the prompt \'Begin\' !'
    time.sleep(2)
    print 'Begin !'
    os.system('arecord -D sysdefault:CARD=1 -c 1 -f S16 -r 8000 -d 3 /home/pi/DPCodes/Modules/recog.wav')
    #file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)),'recog.wav')
    file_name = '/home/pi/DPCodes/Modules/recog.wav'
    fs, signal = wav.read(file_name)
    #signal = signal[:,0]

    ############# Extract MFCC features #############
    mfcc = speechpy.feature.mfcc(signal, sampling_frequency=fs, frame_length=0.020, frame_stride=0.01,
             num_filters=40, fft_length=512, low_frequency=0, high_frequency=None)
    mfccset={}
    mfccset['unknown']=mfcc
    with open('unknownsample.dat','wb') as writef:
        pickle.dump(mfccset,writef,protocol=pickle.HIGHEST_PROTOCOL)
    mfccset={}
    with open('mfccdataset.dat','rb') as readf:
        mfccset=pickle.load(readf)
    if(len(mfccset)==0):
        return 'No Data'
    mfccdata = mfccset.values()
    mfcckeys = mfccset.keys()
    n = len(mfccdata)
    with open('unknownsample.dat','rb') as readf:
        aset=pickle.load(readf)
    a=aset.values()[0]
    mindist = 10000.000
    minind=-1
    for i in range(n):
        b=mfccdata[i]
        cost_matrix, alignmend_a, alignmend_b = dtw2d(a, b)
        r,l=cost_matrix.shape
        cost=cost_matrix[r-1][l-1]
        #print "Distance between ",mfcckeys[i]," and given voice is:\t",cost_matrix[r-1][l-1]
        if cost<mindist:
            mindist=cost
            minind=i
    if mindist>=2500 or minind==-1:
        return 'Not Found'
    elif mindist>=2000:
        return 'Not Accurate'
    else:
        return str(mfcckeys[minind])

def delete(keyid):

    keyid=str(keyid)
    mfccset={}
    if os.path.exists('mfccdataset.dat'):
        with open('mfccdataset.dat','rb') as readf:
            mfccset=pickle.load(readf)
    keys = mfccset.keys()
    hasFlag=False
    for key in keys:
        if key==keyid:
            hasFlag=True
            break
    if hasFlag==False:
        return 'Key Not Present'
    del mfccset[keyid]
    with open('mfccdataset.dat','wb') as writef:
        pickle.dump(mfccset,writef,protocol=pickle.HIGHEST_PROTOCOL)
    print 'Successfully deleted',keyid,'from the database!'
    return 'Done'
