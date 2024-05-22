import cv2
import numpy as np
import face_recognition
import os
import datetime
import pyfirmata
from utils import mark_attendance, parse_encodings, make_face_box
import time


path = 'all-images'
images = []
classNames = []
images_name = os.listdir(path)
p_time, c_time = 0, 0

print(images_name)

for cl in images_name:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

print(classNames)



encoding_list_known = parse_encodings(images)
print("Encoding Complete")


board = pyfirmata.Arduino('/dev/ttyUSB0')
print("Communication Successfully started")

led_light = board.get_pin('d:7:o')
led_light.write(1)

buzzer = board.get_pin('d:12:o')
buzzer.write(1)

cap = cv2.VideoCapture(0)
i = 0

unknown_found = False
buzzerCounter = 0

def show_fps():
    global p_time, c_time
    c_time = time.time()
    fps = 1/(c_time - p_time)
    p_time = c_time

    cv2.putText(img,str(int(fps)), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255,255,255),2)

while True:
    success,img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
    now = datetime.datetime.now()

    show_fps()

    if unknown_found:
        buzzerCounter += 1
        if buzzerCounter > 10:
            buzzerCounter = 0
            unknown_found = False
            buzzer.write(1)

    for encodeFace, faceLoc in zip(encodeCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encoding_list_known,encodeFace)
        faceDis = face_recognition.face_distance(encoding_list_known,encodeFace)
        matchIndex = np.argmin(faceDis)


        y1,x2,y2,x1 = faceLoc

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            make_face_box(img, x1, y1, x2, y2, (0, 255, 0), name)
            mark_attendance(name, led_light)
        else:
            make_face_box(img, x1, y1, x2, y2, (0, 0, 255))

            if not os.path.exists('Unknown'):
                os.makedirs('Unknown')
            cv2.imwrite('Unknown/Unkown' + str(i) + '.jpg', img)

            # blink_pcb(0.01, buzzer)
            buzzer.write(0)
            unknown_found = True
            buzzerCounter = 0
            i += 1


    cv2.imshow('Attendance',img)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()

led_light.write(1)
buzzer.write(1)
