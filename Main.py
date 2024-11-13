import cv2
import os
import pymysql
from datetime import datetime
from deepface import DeepFace
import time

#INITIALIZE GLOBAL VARIABLES
counter = 0
face_match = False

#DEFINE FUNCTIONS
#This function fixes images that may be missing EOS markers
def detect_and_fix(img_path, img_name):
    # detect for premature ending
    try:
        with open( img_path, 'rb') as im :
            im.seek(-2,2)
            if im.read() == b'\xff\xd9':
                print('Image OK :', img_name) 
            else: 
                # fix image
                img = cv2.imread(img_path)
                cv2.imwrite( img_path, img)
                print('FIXED corrupted image :', img_name)           
    except(IOError, SyntaxError) as e :
      print(e)
      print("Unable to load/write Image : {} . Image might be destroyed".format(img_path) )

#This function fetches user pictures from the database and stores them locally
def fetch_pictures(user_image_dir):
    try:
        connection = pymysql.connect(
            host = "capstone.cd0eiocok9m6.us-east-1.rds.amazonaws.com",
            user = "CapstoneAdmin",
            password = "Capstone12#$",
            database = "SATS",
            port = 3306
            )
        
        with connection.cursor() as cursor:
            sql = "SELECT p.userid, p.picture FROM Pictures p JOIN Enrollment e ON p.userid = e.userid JOIN Classes c ON e.classid = c.classid WHERE c.classid = 5"
            cursor.execute(sql)
            results = cursor.fetchall()
        
        if not os.path.exists(user_image_dir):
            os.makedirs(user_image_dir)

        counter = 1
        for row in results:
            userid = row[0]
            image_blob = row[1]
            
            folder_path = os.path.join(user_image_dir, str(userid))
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                
            image_path = f'{folder_path}/picture_{counter}.jpg'
            
            with open(image_path, 'wb') as file:
                file.write(image_blob)
                
            detect_and_fix(image_path, f'picture_{counter}')

            counter += 1
            
            
    except pymysql.MySQLError as e:
        print(f"Error connecting to database: {e}")
        
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("DB connection closed")

#This function checks whether or not the user has been marked for attendance already
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
            mark_attendance(userid, 5)
            
    except pymysql.MySQLError as e:
        print(f"Error connecting to database: {e}")
        
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("DB connection closed")
            
#This function marks a user's attendance in the database
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

#This function checks the current image against attendance group images for a positive match and marks attendance if a match occurs
def verify_face(image_path):
    global face_match
    data_dir = "/home/ubuntu/user_images"
    
    #current = cv2.imwrite("/home/ubuntu/current.jpeg", frame)
    
    for directory in os.listdir(data_dir):
        for file in os.listdir(os.path.join(data_dir, directory)):
            filepath = os.path.join(data_dir, os.path.join(directory, file)) #path of image from database
            userid = directory
            if file.endswith((".jpg", ".jpeg", ".png")):
                try:
                    print(filepath)
                    result = DeepFace.verify(image_path, filepath, enforce_detection=False)
                    if result['verified']:
                        face_match = True
                        print(f'current userid: {userid}')
                        check_attendance(userid)
                        print(result['verified'])
                except ValueError:
                    face_match = False
                    print("face verification exception")

def monitor_directory(image_dir):
    try:
        while True:
            images_to_process = []
            for root, _, files in os.walk(image_dir):
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        image_path = os.path.join(root, file)
                        images_to_process.append(image_path)

            for image_path in images_to_process:
                process_image(image_path)
                os.remove(image_path)

            time.sleep(0.25)
    
    except Exception as e:
        print(f"An error occurred in monitor_directory: {e}")

def process_image(image_path):
    print("processing image...")
    try:
        DeepFace.detectFace(image_path, detector_backend='opencv')
        print("face detected.")
        try:
            verify_face(image_path)
        except Exception as e:
            print(f'Error processing image {image_path}: {e}')
    except:
        print("no face detected.")
    print("image processed...")

#MAIN PROGRAM BODY
def main():
    image_dir = '/home/ubuntu/SATS_images'
    print("Main method")
    fetch_pictures("/home/ubuntu/user_images")
    monitor_directory(image_dir)

main()
