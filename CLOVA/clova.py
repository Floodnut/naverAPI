import os
import sys
from django.forms import widgets
import requests
import json
import cv2
#windows나 gui 환경에서 테스트해보기

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

def process_image(image):
    cv2.imwrite('capture.jpg')
    files = {'image': open('files/test.jpeg', 'rb')}

    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
    response = requests.post(url,  files=files, headers=headers)
    rescode = response.status_code
    if(rescode==200):
        print (response.text)
    else:
        print("Error Code:" + rescode)

    data = response.json()
    show_photo(image)

def show_photo(image, data): #for refactoring
    if(data['info']['faceCount']>0):
        for face in data['faces']:
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
            cv2.imshow("Hello",image)

if __name__ == "__main__":
    cap = cv2.VideoCapture(0) # 0 is main cam
    while True:
        _, frame = cap.read() # _ or ret?
        cv2.imshow('Camera',frame)
        if cv2.waitKey(1) & 0xFF == ord('c'): #for capture
            process_image(frame)
        if cv2.waitKey(1) & 0xFF == 27: #최소한의 대기 & 종료
            break
    cap.release


"""
if(data['info']['faceCount']>0):
    for face in data['faces']:
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
"""


#print(data['info']['faceCount'])

#cv2.imshow("Hello",image)
#cv2.waitKey(0) #무거운 작업이니 대기시간을 줌