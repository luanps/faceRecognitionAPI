import logging
logging.basicConfig(level=logging.INFO)
import sys
import argparse
import time
import numpy as np
import cv2
import pyrealsense as pyrs
from pyrealsense.constants import rs_option
import pdb
from request import Request
from client import  requestService
from recognition import main
from sklearn.preprocessing import normalize
#from tkinter import Tk
#from gui import Gui
NUMFRAMES = 5

'''parse = argparse.ArgumentParser()
parse.add_argument('empresa',type=int,
    help='1 - Dev | 2- ABL | 3-Detran')
parse.add_argument('depth',type=int,
    help='0: 2D | 1:3D')'''
'''parse.add_argument('modo',type=str,
    help='C - cadastro | V - verificação')
parse.add_argument('-chave',type=str,
    help='-chave : chave de cadastro ex: nome, cpf')
args = parse.parse_args()'''

def convert_z16_to_bgr(frame):
    #Performs depth histogram normalization
    hist = np.histogram(frame, bins=0x10000)[0]
    hist = np.cumsum(hist)
    hist -= hist[0]
    rgb_frame = np.empty(frame.shape[:2] + (3,), dtype=np.uint8)

    zeros = frame == 0
    non_zeros = frame != 0

    f = hist[frame[non_zeros]] * 255 / hist[0xFFFF]
    rgb_frame[non_zeros, 0] = 255 - f
    rgb_frame[non_zeros, 1] = 0
    rgb_frame[non_zeros, 2] = f
    rgb_frame[zeros, 0] = 20
    rgb_frame[zeros, 1] = 5
    rgb_frame[zeros, 2] = 0
    return rgb_frame

def if3dFace(depth,ir,bb):

    #reduz tamanho BB face 
    b = [0,0,0,0]
    b[0]  = int(bb[0]*1.05)
    b[1]  = int(bb[1]*1.05)
    b[2]  = int(bb[2]*.9)
    b[3]  = int(bb[3]*.9)
    center = [ int((b[2]-b[0])/2 + b[0]) , int((b[3]-b[1])/2 + b[1])]
   
    pt1 = [float(x) for x in depth[b[0],b[1],]]
    pt2 = [float(x) for x in depth[b[2],b[1],]]
    pt3 = [float(x) for x in depth[b[0],b[3],]]
    pt4 = [float(x) for x in depth[b[2],b[3],]]
    '''cv2.putText(depth,'0',(b[0],b[1]),cv2.FONT_HERSHEY_DUPLEX,1,(0,200,0),1)
    cv2.putText(depth,'1',(b[2],b[1]),cv2.FONT_HERSHEY_DUPLEX,1,(0,200,0),1)
    cv2.putText(depth,'2',(b[0],b[3]),cv2.FONT_HERSHEY_DUPLEX,1,(0,200,0),1)
    cv2.putText(depth,'3',(b[2],b[3]),cv2.FONT_HERSHEY_DUPLEX,1,(0,200,0),1)
    cv2.putText(depth,'4',(center[0],center[1]),cv2.FONT_HERSHEY_DUPLEX,1,(0,200,0),1)'''

    center = [float(x) for x in depth[center[0],center[1]]]
    dif = [pt1,pt2,pt3,pt4,center]
    a,maxx = max(list(zip(dif, range(len(dif)))))
    a,minn = min(list(zip(dif, range(len(dif)))))
    #zeros = [20.0,5.0,0.0]
    zeros = [0.0,0.0,0.0]
    if (zeros == dif[0] == dif[1] == dif[2] ==dif[3] or minn!=4): 
        #dif[-1] == dif[0] or dif[-1] ==dif[1] or dif[-1] == dif[2]):
        return (0,b)

    print(pt1,pt2,pt3,pt4,center)

    #norm 
    '''dR = depth[b[0]:b[2],b[1]:b[3]]
    dRn= np.zeros((dR.shape))
    dRn[:,:,0] = normalize(dR[:,:,0])
    dRn[:,:,1] = normalize(dR[:,:,1])
    dRn[:,:,2] = normalize(dR[:,:,2])
    l1 = np.linalg.norm(dRn[:,:,0])
    l2 = np.linalg.norm(dRn[:,:,1])
    l3 = np.linalg.norm(dRn[:,:,2])
    lb = ' %.1f %.1f %.1f'%(l1,l2,l3)
    cv2.putText(depth,lb,(20,50),cv2.FONT_HERSHEY_DUPLEX,1,(0,200,0),1)'''

    #n pixels random dentro da face
    '''y = np.random.random_integers(low=b[0],high=min(b[2],640),size=10)
    x = np.random.random_integers(low=b[1],high=min(b[3],480),size=10)
    diff = [0,0,0]
    for i in range(0,len(x)):
        diff = abs(depth[x[i],y[i],:] - diff)
        for j in depth[x[i],y[i],:]:
            if j > 200:
                cv2.rectangle(depth,(b[0],b[1]),(b[2],b[3]),(0,0,200),2) 
                return depth'''
                
    

    return (1,b)


with pyrs.Service() as serv:

    with serv.Device() as dev:

        dev.apply_ivcam_preset(0)
        
        try:  # set custom gain/exposure values to obtain good depth image
            custom_options = [(rs_option.RS_OPTION_R200_LR_EXPOSURE, 30.0),
                              (rs_option.RS_OPTION_R200_LR_GAIN, 100.0),
                              (rs_option.RS_OPTION_F200_LASER_POWER, 12)]

            #novas configs - desabilitado
            custom_opt = [(rs_option.RS_OPTION_COLOR_BACKLIGHT_COMPENSATION,1),
                (rs_option.RS_OPTION_COLOR_BRIGHTNESS,55),
                (rs_option.RS_OPTION_COLOR_CONTRAST, 32),
                (rs_option.RS_OPTION_COLOR_ENABLE_AUTO_EXPOSURE,167),
                (rs_option.RS_OPTION_COLOR_GAIN,64),
                (rs_option.RS_OPTION_COLOR_GAMMA,220),
                (rs_option.RS_OPTION_COLOR_HUE, 0),
                (rs_option.RS_OPTION_COLOR_SATURATION, 128),
                (rs_option.RS_OPTION_COLOR_SHARPNESS,0),
                (rs_option.RS_OPTION_COLOR_WHITE_BALANCE, 3200),
                (rs_option.RS_OPTION_F200_ACCURACY, 1),
                (rs_option.RS_OPTION_F200_MOTION_RANGE, 10),
                (rs_option.RS_OPTION_F200_FILTER_OPTION, 5),
                (rs_option.RS_OPTION_F200_CONFIDENCE_THRESHOLD, 1),
                (rs_option.RS_OPTION_F200_LASER_POWER, 12)]

            dev.set_device_options(*zip(*custom_options))
        except pyrs.RealsenseError:
            pass  # options are not available on all devices

        cnt = 0
        last = time.time()
        smoothing = 0.9
        fps_smooth = 30
        bb = 0
        is3d = 0
        while True:
 
            dev.wait_for_frames()
            c = dev.color
            c = cv2.cvtColor(c, cv2.COLOR_RGB2BGR)

            if bb:
                cv2.rectangle(c,(bb[0],bb[1]),(bb[2],bb[3]),(0,200,0),2) 
                cv2.putText(c,'%s'%chave,(bb[0],bb[1]),cv2.FONT_HERSHEY_DUPLEX,2,(100,200,0),2)

            #if args.depth:
            d = dev.depth# * dev.depth_scale * 1000
            pc = dev.pointcloud 
            d = convert_z16_to_bgr(d)
            
            
            #d = cv2.applyColorMap(d.astype(np.uint8), cv2.COLORMAP_RAINBOW)
            if bb:
                try:
                    is3d,b = if3dFace(pc,i,bb)
                    if is3d:
                        cv2.rectangle(d,(b[0],b[1]),(b[2],b[3]),(0,200,0),2) 
                        cv2.putText(d,'%s'%chave,(b[0],b[1]),cv2.FONT_HERSHEY_DUPLEX,2,(100,200,0),2)

                except:
                    pass
                    
            i = dev.infrared
            i = i.reshape(i.shape[0],i.shape[1],1)
            i = cv2.cvtColor(i.astype(np.uint8),cv2.COLOR_GRAY2BGR)
            cd = np.concatenate((c, d, i), axis=1)
            cv2.imshow('', cd)
            #else:
            #    cv2.imshow('', c)

            cnt += 1
            if (cnt % NUMFRAMES) == 0 and cnt >50:
                now = time.time()
                dt = now - last
                fps = NUMFRAMES/dt
                fps_smooth = (fps_smooth * smoothing) + (fps * (1.0-smoothing))
                last = now
                bb=0
                identify = requestService('000003-imgWebcam-0001-1-1111-11111.jpg',c,1,1)
                print(main(identify))
                #identify = main([Request('00000%d-imgWebcam-0001-1-1111-11111.jpg'%args.empresa,
                #    c,1)])
                '''try:
                    chave = identify[0][0][0]
                    bb = identify[0][2]
                except:
                    pass'''

            
            #c = cv2.rectangle(c,(100,100),(250,250),(0,200,0),2)
            #box1= c[200:400,300:500,:]
            #box2= d[200:400,300:500,:]

            #cv2.putText(cd, str(fps_smooth)[:4], (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0))
            #cd = np.concatenate((box1,box2), axis=1)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
