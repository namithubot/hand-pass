import cv2 as cv
import tkinter as tk
import sqlite3

from gesture_recognizer import get_gesture_name, get_gesture_name_custom
from utils import write_on_image, hash_gesture

con = sqlite3.connect('gesture.db')
# Only for first run
# con.execute("CREATE TABLE user(user, password)")
def is_landmark_equal(landmarks1, landmarks2):
    if (len(landmarks1) != len(landmarks2)):
        return False
    for l1, l2 in zip(landmarks1, landmarks2):
        for l12, l22 in zip(l1, l2):
            if round(l12.x, 2) != round(l22.x, 2) or round(l12.y, 2) != round(l22.y, 2):
                return False
    return True


#image = cv.cvtColor(cv.imread('image.jpg'), cv.COLOR_BGR2RGB)
# image = mp.Image.create_from_file("image.jpg")

password = ''
entered_password = []
unhashed_password = []
password_unhashed = []
input = []
isRecording = False
isEntering = False
escape_gesture = 'paper'
mode = 'None'
last_gesture = ''

use_mp = True
times = []

cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")



def start():
    global password, entered_password, unhashed_password, input, isRecording
    global isEntering
    global escape_gesture
    global mode
    global last_gesture
    password_unhashed = globals()['password_unhashed']
    
    use_mp = True
    times = []
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        key_pressed = cv.waitKey(1)
        if key_pressed == ord('r'):
            isRecording = True
            isEntering = False
            mode = 'Rec'
            last_gesture = ''
            print("Recorded keypoint")
        elif key_pressed == ord('e'):
            isRecording = False
            isEntering = True
            mode = 'Enteringqq'
            last_gesture = ''
            print(password)
        elif key_pressed == ord('c') and not isEntering:
            print('clear password')
            entered_password = []
            password_unhashed = []
        elif key_pressed == ord('c') and isEntering:
            unhashed_password = []
            entered_password = []
        elif key_pressed == ord('q') or (isEntering and entered_password == password):
            print('success')
            print(times)
            print(sum(times)/len(times))
            if isRecording and entered_password != []:
                password = hash_gesture(''.join(entered_password))
            break
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        # gray = cv.cvtColor(frame, cv)
    
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        if use_mp:
            gesture_name = get_gesture_name(frame, times)
        else:
            gesture_name = get_gesture_name_custom(frame)
    
        if gesture_name not in ['unrecognized', 'none', ''] and gesture_name != last_gesture:
            gesture_hash = hash_gesture(gesture_name)
            if isRecording:
                if gesture_name != escape_gesture:
                    entered_password.append(gesture_hash)
                    password_unhashed.append(gesture_name)
            elif isEntering:
                    #password_unhashed.pop(0)
                    entered_password.append(gesture_hash) #password.pop(0)
                    print(password == entered_password)
                    print(password)
                    print(entered_password)
            last_gesture = gesture_name
    
        # STEP 5: Process the classification result. In this case, visualize it.
        annotated_image = cv.cvtColor(write_on_image(frame, mode + ' ' + gesture_name + ':' + ",".join(password_unhashed), 50, 50), cv.COLOR_RGB2BGR)
        face = cascade.detectMultiScale(
            annotated_image, scaleFactor=2.0, minNeighbors=4)
    
        for x, y, w, h in face:
    
            # draw a border around the detected face.  
            # (here border color = green, and thickness = 3) 
            annotated_image = cv.rectangle(annotated_image, (x, y), (x+w, y+h),
                                  (0, 255, 0), 3)
    
            # blur the face which is in the rectangle 
            annotated_image[y:y+h, x:x+w] = cv.medianBlur(annotated_image[y:y+h, x:x+w],
                                                 35)
        # Display the resulting frame
        cv.imshow('frame', annotated_image)
    
    cap.release()
    cv.destroyAllWindows()

def open_folder():
    import os
    path = os.path.realpath('.')
    os.startfile(path)

def record():
    global isRecording, isEntering, mode, password, entered_password, unhashed_password, password_unhashed
    password = []
    unhashed_password = []
    password_unhashed = []
    mode = 'Rec'
    isRecording = True
    isEntering = False
    start()
    if password != '':
        if None != con.execute(f"SELECT 1 FROM user WHERE user = '{username.get()}'").fetchone():
            con.execute(f"UPDATE user SET password = '{password}' WHERE user = '{username.get()}'")
        else:
            con.execute(f"INSERT INTO user VALUES('{username.get()}', '{password}')")
        con.commit()
    unhashed_password = password_unhashed

def enter():
    global isRecording, isEntering, mode, password, entered_password, unhashed_password, password_unhashed
    mode = 'Entering'
    isEntering = True
    isRecording = False
    entered_password = []
    password_unhashed = unhashed_password
    password = con.execute(f"SELECT password FROM user WHERE user = '{username.get()}'").fetchone()[0]
    start()
    if password != '' and password == hash_gesture(''.join(entered_password)):
        tk.Message(window, width=45, text='Success', command= open_folder()).pack()
    else:
        tk.Message(window, width=45, text='Failure').pack()

window = tk.Tk()
button = tk.Button(window, text='Record', width=45, command=lambda: record())
button2 = tk.Button(window, text='Enter', width=45, command=lambda: enter())
username = tk.Entry(window, width=45)
username.pack()
button.pack()
button2.pack()
window.mainloop()