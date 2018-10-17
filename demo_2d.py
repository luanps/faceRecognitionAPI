import cv2
import sys
import argparse
import pdb
from request import Request
from recognition import main
NUMFRAMES = 5
parse = argparse.ArgumentParser()
parse.add_argument('empresa',type=int,
    help='1 - Dev | 2- ABL | 3-Detran')
'''
parse.add_argument('3d',type=int,
    help='0: 2D | 1:3D')
parse.add_argument('modo',type=str,
    help='C - cadastro | V - verificação')
parse.add_argument('-chave',type=str,
    help='-chave : chave de cadastro ex: nome, cpf')'''

args = parse.parse_args()
cap = cv2.VideoCapture(0)
         
count = 0
bb=0

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

    if (count%NUMFRAMES==1):
        bb=0
        identify = main([Request('00000%d-imgWebcam-0001'%args.empresa,frame,1)])
        try:
            chave = identify[0][0][0]
            bb = identify[0][2]
            
        except:
            pass

cap.release()
cv2.destroyAllWindows()

