import threading
import pandas as pd
import cv2
from deepface import DeepFace

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0
face_match = False

def find_face(frame):
    global face_match
    cv2.imwrite("current.jpg", frame)
    cv2.imshow("current", cv2.imread("current.jpg"))
    print("inside")
    df = DeepFace.find(img_path = cv2.imread("./current.jpg"), db_path = "./Pictures/Faces/")

    print(df.head())
    
while True:
    
    ret, frame = cap.read()

    if ret:
        if counter % 15 == 0:
            try:
                threading.Thread(target=find_face, args=(frame,)).start()
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