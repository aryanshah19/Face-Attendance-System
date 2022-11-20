import face_recognition
import cv2
import os
import time
import numpy as np
from datetime import date
today = date.today()
from helperfunctions import findEncodings, markAttendance, importstudentdata, \
    generate_hash_dict, send_message, send_photo, read_bc, read_barcodes
import qrcode

Project_path = "/Users/aryan/Desktop/Attendance System/QR_Code_Images/"

class my_dictionary(dict):

    # __init__ function
    def __init__(self):
        self = dict()

    # Function to add key:value
    def add(self, key, value):
        self[key] = value


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


matchIndex = np.argmin(faceDis)
rollno = ""
if faceDis[matchIndex] < 0.50:
    #name = className[matchIndex].upper()
    rollno = className[matchIndex].upper()
    #markAttendance(name)
else:
    rollno = False
    #markAttendance(name)

if rollno:
    data, list_of_students = importstudentdata("data.csv")
    dict_names = my_dictionary()
    dict_names = generate_hash_dict(list_of_students, dict_names, data)
    #print(dict_names)
    rollno_hash = str(dict_names[rollno][1])
    img = qrcode.make(dict_names[rollno][1])
    qr_code_path = Project_path + str(rollno) + '.jpg'
    img.save(qr_code_path)

    message = "Hello! " + rollno + " Here's Your QR code for " + str(date.today())
    send_message(message)
    send_photo(qr_code_path)

    qr_hash = read_bc()

    if rollno_hash == qr_hash:
        message_text = rollno + "-" + data.loc[rollno]["Name"] + " is present."
        print(message_text)
    else:
        print("Couldn't verify the two methods, please try again")

    markAttendance(rollno, data)







