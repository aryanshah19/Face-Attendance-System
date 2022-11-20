import face_recognition
import cv2
from csv import writer
from datetime import datetime, date
import hashlib
today = date.today()
import pandas as pd
import requests
from pyzbar import pyzbar
import time



def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(rollno,data):
    with open('Attendance.csv', 'a') as f:
        writer_object = writer(f)
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        d = today.strftime("%b-%d-%Y")
        row = [rollno, data.loc[rollno]["Name"], dt_string, d]
        writer_object.writerow(row)
        f.close()
        # f.writelines(f'{name},{dt_string},{d}')


def importstudentdata(csvpath):
    df = pd.read_csv(csvpath, index_col=None)
    df = df.reset_index().set_index('Rollno')
    df.drop("index", inplace=True, axis=1)
    list_of_roll = []
    for i in df.index:
        list_of_roll.append(i)
    return df, list_of_roll


def generate_hash_dict(list_of_students, dict_names, data):
    for i in list_of_students:
        string = data.loc[i]["Name"].replace(" ", "") + str(i) + str(date.today())
        hash_generated = hashlib.sha256(string.encode('utf-8')).hexdigest()[0:10]
        dict_names.add(i, [string, hash_generated])
    return dict_names

def send_photo(image):

    apiToken = ""
    chatID = ""
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendPhoto'

    try:
        response = requests.post( apiURL, data={'chat_id':chatID},
                                 files={'photo': open(image, 'rb')})
        #print(response.text)
    except Exception as e:
        print(e)

def send_message(message):
    apiToken = ""
    chatID = ""
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        #print(response.text)
    except Exception as e:
        print(e)



def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    barcode_info = ""
    for barcode in barcodes:
        barcode_info = barcode.data.decode('utf-8')
    return frame, barcode_info


def read_bc():
    # 1
    camera = cv2.VideoCapture(0)
    time.sleep(5)
    ret, frame = camera.read()
    frame, barcode_info = read_barcodes(frame)
    cv2.imshow('Barcode/QR code reader', frame)
    cv2.waitKey(0)
    camera.release()
    cv2.destroyAllWindows()
    return barcode_info

