import requests 
import cv2 
import numpy as np 
import time
import face_recognition
import os
import datetime
from utils import make_face_box, parse_encodings

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

i = 0

unknown_found = False
buzzerCounter = 0

def show_fps():
    global p_time, c_time
    c_time = time.time()
    fps = 1/(c_time - p_time)
    p_time = c_time

    cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)

url = "http://192.168.1.103:8080/shot.jpg"
has_ip_cam = True
try:
    img_resp = requests.get(url, timeout=2)
except:
    has_ip_cam = False

video = cv2.VideoCapture(0)

while True:
    if has_ip_cam:
        img_resp = requests.get(url, timeout=1)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8) 
        img = cv2.imdecode(img_arr, -1)
        # img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        height, width, _ = img.shape
        if height > 640:
            img = cv2.resize(img, (int(width * 640 / height), 640))

    else:
        ret, img = video.read()

    img = cv2.flip(img, 1)

    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(img)
    encodeCurFrame = face_recognition.face_encodings(img, facesCurFrame)
    now = datetime.datetime.now()

    show_fps()

    for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encoding_list_known, encodeFace)
        faceDis = face_recognition.face_distance(encoding_list_known, encodeFace)
        matchIndex = np.argmin(faceDis)

        y1, x2, y2, x1 = faceLoc

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            make_face_box(img, x1, y1, x2, y2, (0, 255, 0), name)
        else:
            make_face_box(img, x1, y1, x2, y2, (0, 0, 255))

            if not os.path.exists('Unknown'):
                os.makedirs('Unknown')
            cv2.imwrite('Unknown/Unkown' + str(i) + '.jpg', img)

            unknown_found = True
            buzzerCounter = 0
            i += 1

    cv2.imshow('Attendance', img)
    if cv2.waitKey(1) == 27:
        break

video.release()
cv2.destroyAllWindows()