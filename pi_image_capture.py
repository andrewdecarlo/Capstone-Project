import cv2
import os
import requests
import subprocess
from datetime import datetime

cap = cv2.VideoCapture(0, cv2.CAP_V4L)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

ret, frame = cap.read()

timestamp = datetime.now()
image_path = f"image_{timestamp}.jpg"
cv2.imwrite(image_path, frame)

cap.release()

url = "http://3.88.171.10:5000/upload"
files = {'file': open(image_path, 'rb')}
response = requests.post(url, files=files)

"""
remote_path = f'{user}@{ip}:/home/ubuntu/SATS_images'

scp_command = ["scp", "-i", pem_file_path, image_path, remote_path]

try:
    subprocess.run(scp_command, check=True)
except subprocess.CalledProcessError as e:
    print(e)
"""

#os.remove(image_path)