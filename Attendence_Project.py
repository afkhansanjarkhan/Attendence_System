import os
from datetime import datetime
import mysql.connector
import cv2
import face_recognition
import numpy as np

images = []
images_names = []
myList = os.listdir('.')
#print(myList)

Given_time = '10:00:00 AM'


def Create_Database(databaseName):
    mydb = mysql.connector.connect(locahost="localhost",port="8000",passwd="student123")
    mycursor = mydb.cursor()
    mycursor.execute('create database {databaseName}')
    mycursor.execute('create table student_data(id int(200),name varchar(200),date DATETIME,attendence BOOLEAN)')

def Insert_Database(databaseName,name,time,attendence):
    mydb  = mysql.connector.connect(localhost="localhost",port="8000",passwd="student123",database=databaseName)
    mycursor = mydb.cursor()
    mycursor.execute("insert into {databaseName} values({name},{time},{attendence})")
def show_data(databaseName,table_name):
    mydb = mysql.connector.connect(locahost="localhost", port="8000", passwd="student123",database=databaseName)
    mycursor = mydb.cursor()
    mycursor.execute('select * from {table_name}')



for single_image in myList:
    if(os.path.splitext(single_image)[1]!='.py'):
        curImage = cv2.imread(f'{single_image}')
        images.append(curImage)
        images_names.append(os.path.splitext(single_image)[0])
print(images_names)

def findEnocdings(images):
    encoding_list = []
    for img in images:
        #img=np.full((100,80,3),12,dtype=np.uint8)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img_encoding = face_recognition.face_encodings(img)
        encoding_list.append(img_encoding)
    return encoding_list







encodedListKnown = findEnocdings(images)
#print(encodedListKnown)
print("Encoding Completed")


cap = cv2.VideoCapture(0)

while True:
    succes,img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(imgS)
    faceEncodingCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)


    for encodeFace,faceLoc in zip(faceEncodingCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodedListKnown,encodeFace)

        facedistance  = face_recognition.face_distance(encodedListKnown,encodeFace)
        print("printing face Distnace")
        #print(facedistance)
        matchIndex = np.argmin(facedistance)

        if matches[matchIndex]:
            name=images_names[matchIndex].upper()
            time = datetime.time(datetime.now())
            v_time = time.strftime("%I:%M:%S %p")
            if(v_time==Given_time):
                attendence= True
                print(name)

                x1,x2,y1,y2=faceLoc
                x1,x2,y1,y2=x1*4,x2*4,y1*4,y2*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0),3)
                cv2.rectangle(img,(x1,y1-35),(x2,y2),(255,0,0),3)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)

                cv2.imshow("webcam",img)
                cv2.waitKey(1)

databaseName = "attendence_data"
Create_Database(databaseName)
Insert_Database(databaseName,name,time,attendence)
show_data(databaseName,table_name)
