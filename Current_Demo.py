import threading
import pandas as pd
import cv2
from deepface import DeepFace

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


counter = 0

reference_img = cv2.imread("pictures/faces/test.jpg")

face_match = False


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
        facematch = DeepFace.find(img_path=cv2.imread("current.jpg"), db_path="./Pictures/Faces")
        try:
            trymatch = DeepFace.find(cv2.imread("current.jpg"), "./Pictures/Faces")
            if trymatch:
                face_match = True
                print(trymatch['identity'])
            else:
                face_match = False
        except:
            print("Assertion Failed.")
    except ValueError:
        print("ValueError :(")
        face_match = False

def write_image(frame):
    cv2.imwrite("image.jpg", frame)
    print("image written")

while True:
    ret, frame = cap.read()

    if ret:
        if counter % 60 == 0:
            try:
                threading.Thread(target=find_face, args=(frame.copy(),)).start()
            except ValueError:
                print("no face")
                pass
        counter += 1
        
        if face_match:
            cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cv2.destroyAllWindows()
