'''
Client side example:
Captures a user's image from webcam and makes an example query on server.
'''
import cv2
import sys
import argparse
import pdb
from request import Request
from recognition import main,toBase64,toImage
from client import requestService
import random
import json
import requests

NUMFRAMES = 5
"""
parse = argparse.ArgumentParser()
parse.add_argument('empresa',type=int,
    help='1 - Dev | 2- ABL | 3-Detran')
parse.add_argument('3d',type=int,
    help='0: 2D | 1:3D')
parse.add_argument('modo',type=str,
    help='C - cadastro | V - verificação')
parse.add_argument('-chave',type=str,
    help='-chave : chave de cadastro ex: nome, cpf')

args = parse.parse_args()"""
cap = cv2.VideoCapture(0)
         
count = 0
bb=0

print('Pressione "espaco" para tirar foto e comparar com banco de dados, pressiona "q" para sair\n')
print('Press "space" to take a picture from webcam and make a comparison with the database. Press "q" to exit\n')
 
while cap.isOpened():
    ret,frame = cap.read()

    if bb:
        cv2.rectangle(frame,(bb[0],bb[1]),(bb[2],bb[3]),(0,200,0),2)
        cv2.putText(frame,'%s'%chave,(bb[0],bb[1]),cv2.FONT_HERSHEY_DUPLEX,2,(0,200,0),2)
    cv2.imshow('WebCam',frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    count +=1

    if key == 32: #space button #(count%NUMFRAMES==1):
        bb=0
        frame = str(toBase64(frame))
        identify = requestService('00003-WebCam-00001-1-11111-111111.jpg',frame,1,2)
        data = json.dumps(identify.__dict__)
        #print(main(identify))
        #res = requests.post("http://127.0.0.1:5000",json=json.dumps({'key':'value'}))#.json()
        res = requests.post("http://127.0.0.1:5000",json=data)
        print(res.text)
        #new = json.loads(data)

        '''try:
            chave = identify[0][0][0]
            #bb = identify[0][2]
            
        except:
            pass'''

cap.release()
cv2.destroyAllWindows()

