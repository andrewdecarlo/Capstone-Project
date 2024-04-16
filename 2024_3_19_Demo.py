import cv2
import face_recognition

#Read image into var
andrew = cv2.imread("pictures/faces/Andrew.jpeg")
#Convert from BGR format to RGB
andrew = cv2.cvtColor(andrew, cv2.COLOR_BGR2RGB)
#Encode Image
andrew = face_recognition.face_encodings(andrew)[0]

#Repeat image read, conversion, and encoding for 3 other images
pups = cv2.imread("pictures/faces/AndrewTayPups.jpeg")
pups = cv2.cvtColor(pups, cv2.COLOR_BGR2RGB)
pups = face_recognition.face_encodings(pups)[0]

dad = cv2.imread("pictures/faces/AndrewDad.jpeg")
dad = cv2.cvtColor(dad, cv2.COLOR_BGR2RGB)
dad = face_recognition.face_encodings(dad)[0]

andrew2 = cv2.imread("pictures/faces/Andrew2.jpeg")
andrew2 = cv2.cvtColor(andrew2, cv2.COLOR_BGR2RGB)
andrew2 = face_recognition.face_encodings(andrew2)[0]

#Compare images and display result
result = face_recognition.compare_faces([andrew, andrew2, pups, dad], andrew)
print("\nRESULT\n___________________________\n\n", result, "\n\n___________________________\n\n")
