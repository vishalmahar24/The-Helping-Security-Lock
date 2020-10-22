import zbar
import os
import pickle
def train(keyid):
    all_bars={}
    if os.path.exists('dataset_bar.dat'):
        with open('dataset_bar.dat','rb') as rf:
            all_bars = pickle.load(rf)
    print "Please place the ID card near the camera:"
    proc = zbar.Processor()

    proc.parse_config('enable')

    device = '/dev/video0'
    proc.init(device)

    proc.visible = True

    proc.process_one()
    result=''

    for symbol in proc.results:
        #print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        result=symbol.data
    all_bars[str(keyid)]=result
    with open('dataset_bar.dat','wb') as wf:
                pickle.dump(all_bars,wf)
    print 'Successfully added',keyid,'to the database!'

def recog():
    all_bars={}
    if os.path.exists('dataset_bar.dat'):
        with open('dataset_bar.dat','rb') as rf:
            all_bars = pickle.load(rf)
    if len(all_bars)==0:
        return 'No Data'
    all_keys = all_bars.keys()
    all_values = all_bars.values()
    print "Please place the ID card near the camera:"
    proc = zbar.Processor()

    proc.parse_config('enable')

    device = '/dev/video0'
    proc.init(device)

    proc.visible = True

    proc.process_one()
    result=''
    for symbol in proc.results:
        #print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        result=symbol.data
    for i in range(len(all_keys)):
        if all_values[i]==result:
            return all_keys[i]
    return 'Not Found'

def delete(keyid):

    keyid=str(keyid)
    barset={}
    if os.path.exists('dataset_bar.dat'):
        with open('dataset_bar.dat','rb') as readf:
            barset=pickle.load(readf)
    keys = barset.keys()
    hasFlag=False
    for key in keys:
        if key==keyid:
            hasFlag=True
            break
    if hasFlag==False:
        return 'Key Not Present'
    del barset[keyid]
    with open('dataset_bar.dat','wb') as writef:
        pickle.dump(barset,writef,protocol=pickle.HIGHEST_PROTOCOL)
    print 'Successfully deleted',keyid,'from the database!'
    return 'Done'
