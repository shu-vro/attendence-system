import cv2
import numpy as np
import face_recognition
import os
import datetime
import datetime


path = 'all-images'
images = []
classNames = []
images_name = os.listdir(path)

print(images_name)

for cl in images_name:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

print(classNames)


def mark_attendance(name):
    if not os.path.exists('Attendance.csv'):
        with open('Attendance.csv', 'w') as csv_file:
            csv_file.write('Name,Date,Time')
    with open('Attendance.csv', 'r+') as csv_file:
        myDataList = csv_file.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.datetime.now()
            date = now.strftime('%D')
            time = now.strftime("%I:%M:%S %p")
            csv_file.writelines(f'\n{name},{date},{time}')

def parse_encodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encoding_list_known = parse_encodings(images)
print("Encoding Complete")


cap = cv2.VideoCapture(0)
i = 0
while True:
    success,img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
    now = datetime.datetime.now()

    for encodeFace,faceLoc in zip(encodeCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encoding_list_known,encodeFace)
        faceDis = face_recognition.face_distance(encoding_list_known,encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)


        y1,x2,y2,x1 = faceLoc

        if matches[matchIndex]:
            print(matches[matchIndex])
            name = classNames[matchIndex].upper()
            #y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2), (x2, y2+35), (0, 255, 0), cv2.FILLED)
            cv2.putText(img,name, (x1, y2), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255,255,255),2)
            mark_attendance(name)
        else:
            # y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(img, (x1, y2), (x2, y2+35), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, "Unknown", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)

            if not os.path.exists('Unknown'):
                os.makedirs('Unknown')
            cv2.imwrite('Unknown/Unkown' + str(i) + '.jpg', img)

            i += 1


    cv2.imshow('Attendance',img)
    if cv2.waitKey(1) == 27:  # 27 is the ASCII value of the ESC key
        break

cap.release()
cv2.destroyAllWindows()
