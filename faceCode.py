import face_recognition
import pickle
import cv2
import glob
import os
import doorcheck
import servoCode

def train(keyid):

    video_capture = cv2.VideoCapture(0)
    face_stored = False
    all_face_encodings = {}
    if os.path.exists('dataset_faces.dat'):
        with open('dataset_faces.dat','rb') as rf:
            all_face_encodings = pickle.load(rf)

    curr_path = os.getcwd()+'/db_faces/'

    '''
    file_no = 0
    list_of_files = glob.glob(curr_path+'*')

    if len(list_of_files) == 0:
        file_no=1
    else:
        latest_file = max(list_of_files,key=os.path.getctime)
        file_no=int(latest_file[56:-4])
        file_no+=1
    '''
    while face_stored==False:

        ret,frame = video_capture.read()
        small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
        rgb_small_frame = small_frame[:,:,::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        if len(face_locations)==1:
            print "Found a face! Writing face to memory as",str(keyid),".jpg !"
            top,right,bottom,left = face_locations[0]
            top *=4
            right *=4
            left *=4
            bottom *=4
            cv2.imwrite(curr_path+str(keyid)+'.jpg',frame)
            cv2.rectangle(frame,(left,top),(right,bottom),(0,255,0),2)
            all_face_encodings[str(keyid)] = face_recognition.face_encodings(rgb_small_frame,face_locations)[0]
            with open('dataset_faces.dat','wb') as wf:
                pickle.dump(all_face_encodings,wf)
            face_stored = True
        #else:
        #    print "Face not found!"
        cv2.imshow('Video',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
           break

    video_capture.release()

    cv2.destroyAllWindows()



def recog():
    video_capture = cv2.VideoCapture(0)

    # Create arrays of known face encodings and their names
    all_face_encodings = {}
    with open('dataset_faces.dat','rb') as rf:
        all_face_encodings = pickle.load(rf)
    if(len(all_face_encodings)==0):
        return 'No Data'
    known_face_names = list(all_face_encodings.keys())
    known_face_encodings = list(all_face_encodings.values())

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the face encodings in the current frame of video
            face_encodings = face_recognition.face_encodings(rgb_small_frame)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding,0.45)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame
        if len(face_names)==1:
            if face_names[0]!="Unknown":
                video_capture.release()
                cv2.destroyAllWindows()
                return face_names[0]

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    return 'Not Found'

def delete(keyid):

    keyid=str(keyid)
    faceset={}
    if os.path.exists('dataset_faces.dat'):
        with open('dataset_faces.dat','rb') as readf:
            faceset=pickle.load(readf)
    keys = faceset.keys()
    hasFlag=False
    for key in keys:
        if key==keyid:
            hasFlag=True
            break
    if hasFlag==False:
        return 'Key Not Present'
    del faceset[keyid]
    with open('dataset_faces.dat','wb') as writef:
        pickle.dump(faceset,writef,protocol=pickle.HIGHEST_PROTOCOL)
    print 'Successfully deleted',keyid,'from the database!'
    return 'Done'
