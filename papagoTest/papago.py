import os
import sys
import urllib.request
import json

with open ('../secret.json','r') as key_file:
    json_file = json.load(key_file)
    json_client_id= json_file["client_id"]
    json_client_secret = json_file["client_secret"]

client_id = json_client_id # 개발자센터에서 발급받은 Client ID 값
client_secret = json_client_secret # 개발자센터에서 발급받은 Client Secret 값

encText = urllib.parse.quote("안녕하세요. 여러분")

data = "source=ko&target=en&text=" + encText
url = "https://openapi.naver.com/v1/papago/n2mt"

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)

response = urllib.request.urlopen(request, data=data.encode("utf-8"))
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    #print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)

#print(response)

data = json.loads(response_body)
translatedData = data['message']['result']['translatedText']
print(translatedData)
