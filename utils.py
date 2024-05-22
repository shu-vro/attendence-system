import os, csv, datetime, time
import cv2, face_recognition
from typing import Tuple

def blink_pcb(sec, port):
    port.write(0)
    time.sleep(sec)
    port.write(1)

def mark_attendance(name, buzzer):
    if not os.path.exists('Attendance.csv'):
        with open('Attendance.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Name', 'Date', 'Time'])
    with open('Attendance.csv', 'r+', newline='') as csv_file:
        reader = csv.reader(csv_file)
        nameList = [row[0] for row in reader]
        if name not in nameList:
            now = datetime.datetime.now()
            date = now.strftime('%D')
            time = now.strftime("%I:%M:%S %p")
            blink_pcb(.2, buzzer)
            with open('Attendance.csv', 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([name, date, time])


def make_face_box(img, x1: int, y1: int, x2 : int, y2: int, color: Tuple[int,int,int], name="Unknown"):
    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
    cv2.rectangle(img, (x1, y2), (x2, y2+35), color, cv2.FILLED)
    cv2.putText(img,name, (x1, y2+27), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255,255,255),2)
    pass

def parse_encodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList