import os
import sys
from django.forms import widgets
import requests
import json
import cv2

filename = "files/test.jpeg"
image = cv2.imread(filename)

with open ('../secret.json','r') as key_file:
    json_file = json.load(key_file)
    json_client_id= json_file["clova_id"]
    json_client_secret = json_file["clova_secret"]

client_id = json_client_id # 개발자센터에서 발급받은 Client ID 값
client_secret = json_client_secret # 개발자센터에서 발급받은 Client Secret 값

url = "https://openapi.naver.com/v1/vision/face" # 얼굴감지
#url = "https://openapi.naver.com/v1/vision/celebrity" # 유명인 얼굴인식

files = {'image': open('files/test.jpeg', 'rb')}

headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
response = requests.post(url,  files=files, headers=headers)
rescode = response.status_code
if(rescode==200):
    print (response.text)
else:
    print("Error Code:" + rescode)

data = response.json()
if(data['info']['faceCount']>0):
    for face in data['face']:
        x = face['roi']['x']
        y = face['roi']['y']
        width = face['roi']['height']
        heigth = face['roi']['height']
        print("x={}, y={}, width={}, height={}".format(x,y,width,heigth))
        x1=x
        y1=y
        x2=x1+width
        y2=y1+heigth
        text = face['gender']['value'] + "(" +face['gender']['confidence'] + ")"
        cv2.rectangle(image, (x1,y1),(x2,y2),(0,0,255),2)
        cv2.putText(image,text,(x1,y1-10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),2)


print(data['info']['faceCount'])

cv2.imshow("Hello",image)
cv2.waitKey(0) #무거운 작업이니 대기시간을 줌