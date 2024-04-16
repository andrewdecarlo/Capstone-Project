from deepface import DeepFace
import pandas as pd
import cv2
import matplotlib.pyplot as plt


im = cv2.imread("current.jpeg")
plt.imshow(im[:,:,::-1])
#plt.show()
df = DeepFace.find(im, "./Pictures/Faces")
print(df)
print(df)