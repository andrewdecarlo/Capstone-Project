import threading
import pandas as pd
import cv2
import os
import pymysql
from datetime import datetime
from deepface import DeepFace

print(os.getcwd())
cap = cv2.VideoCapture(0, cv2.CAP_V4L)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


counter = 0

print("Image read")
face_match = False



def fetch_pictures():
    try:
        connection = pymysql.connect(
            host = "capstone.cd0eiocok9m6.us-east-1.rds.amazonaws.com",
            user = "CapstoneAdmin",
            password = "Capstone12#$",
            database = "SATS",
            port = 3306
            )
        
        with connection.cursor() as cursor:
            sql = "SELECT userid, picture FROM Pictures"
            cursor.execute(sql)
            results = cursor.fetchall()
        
        counter = 1
        for row in results:
            userid = row[0]
            image_blob = row[1]
            
            folder_path = f'Capstone-Project/pictures/faces/{userid}'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                
            image_path = f'{folder_path}/picture_{counter}.jpg'
            counter += 1
            
            with open(image_path, 'wb') as file:
                file.write(image_blob)
                
            print(f"Image for user {userid} saved to {image_path}.")
            
    except pymysql.MySQLError as e:
        print(f"Error connecting to database: {e}")
        
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("DB connection closed")

def verify_face(frame):
    global face_match
    data_dir = "Capstone-Project/pictures/faces"
    
    cv2.imwrite("current.jpeg", frame)
    
    for directory in os.listdir(data_dir):
        for file in os.listdir(os.path.join(data_dir, directory)):
            filepath = os.path.join(data_dir, os.path.join(directory, file))
            userid = directory
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                try:
                    print(filepath)
                    result = DeepFace.verify("current.jpeg", filepath, enforce_detection=False)
                    if result['verified']:
                        face_match = True
                        print(f'current userid: {userid}')
                        check_attendance(userid)
                        print(result['verified'])
                except ValueError:
                    face_match = False
                    print("face verification exception")
    

def check_face(frame):
    global face_match
    cv2.imwrite("current.jpg", frame)
    try:
        if DeepFace.verify(cv2.imread("current.jpg"), reference_img.copy())['verified']:

            face_match = True
        else:
            face_match = False
    except ValueError:
        face_match = False

def detect_face(frame):
        global face_match
        cv2.imwrite("current.jpg", frame)
        try:
            print("inside detectface")
            cv2.imshow("current frame", cv2.imread("current.jpg"))
            print()
            if DeepFace.extract_faces(cv2.imread("current.jpg"), (224, 224), "opencv", True, True):
                face_match = True
                print(face_match)
            else:
                pass
                face_match = False
        except ValueError:
            print("ValueError :(")
            face_match = False

def find_face(frame):
    global face_match
    cv2.imwrite("current.jpg", frame)
    try:
        facematch = DeepFace.find(img_path=cv2.imread("current.jpg"), db_path="./pictures/faces")
        try:
            trymatch = DeepFace.find(cv2.imread("current.jpg"), "./pictures/faces")
            if trymatch:
                face_match = True
                print(True)
            else:
                face_match = False
                print(False)
        except:
            print("Assertion Failed.")
    except ValueError:
        print("ValueError :(")
        face_match = False
def write_image(frame):
    cv2.imwrite("image.jpg", frame)
    print("image written")

def check_attendance(userid):
    try:
        connection = pymysql.connect(
            host = "capstone.cd0eiocok9m6.us-east-1.rds.amazonaws.com",
            user = "CapstoneAdmin",
            password = "Capstone12#$",
            database = "SATS",
            port = 3306
            )

        print("connected to database")
        
        cursor = connection.cursor()
        
        current_date = datetime.now().date()
        
        query = f"SELECT * FROM Attendance WHERE userid = %s AND date = %s"
        query_data = (userid, current_date)
        cursor.execute(query, query_data)
        
        results = cursor.fetchone()
        print(results)
        if not results:
            print(f'{userid} not marked')
            mark_attendance(userid, 481)
            
    except pymysql.MySQLError as e:
        print(f"Error connecting to database: {e}")
        
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("DB connection closed")
            

def mark_attendance(userid, classid):
    try:
        connection = pymysql.connect(
            host = "capstone.cd0eiocok9m6.us-east-1.rds.amazonaws.com",
            user = "CapstoneAdmin",
            password = "Capstone12#$",
            database = "SATS",
            port = 3306
            )

        print("connected to database")
        
        cursor = connection.cursor()
        
        current_date = datetime.now().date()
        
        query = "INSERT INTO Attendance (userid, classid, date, present) VALUES (%s, %s, %s, %s)"
        query_data = (userid, classid, current_date, 1)
        
        cursor.execute(query, query_data)
        
        connection.commit()
        print(f"{userid} record successfully commited to DB")
        
    except pymysql.MySQLError as e:
        print(f"Error connecting to database: {e}")
        
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("DB connection closed")


#MAIN
fetch_pictures()
while True:
    ret, frame = cap.read()
    
    if ret:
        
        if counter % 60 == 0:
            try:
                verify_face(frame)
                #threading.Thread(target=verify_face, args=(frame.copy(),)).start()
            except ValueError:
                print("no face")
                pass
        counter += 1
"""      
        if face_match:
            cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        cv2.imshow('video', frame)
        
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
        
cv2.destroyAllWindows()
"""
