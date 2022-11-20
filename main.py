import face_recognition
import cv2
import os
import time
from csv import writer
import numpy as np
from datetime import datetime, date
today = date.today()


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('Attendance.csv', 'a') as f:
        writer_object = writer(f)
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        d = today.strftime("%b-%d-%Y")
        row = [name, dt_string, d]
        writer_object.writerow(row)
        f.close()
        #f.writelines(f'{name},{dt_string},{d}')

path = 'ImagesAttendance'
images = []     # LIST CONTAINING ALL THE # IMAGES
className = []    # LIST CONTAINING ALL THE CORRESPONDING CLASS Names
myList = os.listdir(path)
class_List = []
count = 0
for x,cl in enumerate(myList):
    if cl[-4:] == ".jpg":
        count = count  + 1
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        className.append(os.path.splitext(cl)[0])

print("Total Classes Detected:", count)

encodeListKnown = findEncodings(images)
print('Encodings Complete')

cap = cv2.VideoCapture(0)
time.sleep(1)
success, img = cap.read()

cv2.imshow("test", img)
imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()

facesCurFrame = face_recognition.face_locations(imgS)
encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)



for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
    print(faceDis)

print(faceDis)


matchIndex = np.argmin(faceDis)


if faceDis[matchIndex] < 0.50:
    name = className[matchIndex].upper()
    markAttendance(name)
else:
    name = 'Unknown'
    markAttendance(name)

