'''
Read images from folder and creates a batch of requests.
'''
import sys
import argparse
from os import listdir
from os.path import isfile,join,abspath
import pdb
import cv2
from recognition import main,toImage
from request import Request
import codecs
import numpy as np
import random

#creates a request service given an image
def requestService(imgName,img,appCode,imgType): 

    #request number random
    rn = random.randint(1,1000000)
    #log number random
    log = random.randint(1,1000000)

    #test device  = 123 (insere empresa 1 )
    #test device  DETRAN = 1 (insere empresa 3)
    device = 1

    # our coordinates as test
    lat = -25.450 
    lon = -49.231 

    #image name data
    company,keyPerson,seqPerson = imgName.split('-')[:3]

    #attibutes 
    attr = 0
    #true image default=99
    trueImage = 99
    #true point cloud default=99
    truePC = 99
    #point cloud to be validated default=99
    pc = 99

    return(Request(rn,company,log,device,appCode,lat,lon,keyPerson,attr,
        imgType,trueImage,truePC,img,pc,imgName))


'''def readBase64(path,f,imgType):
    data = []
    for i in listdir(path):
        img = open(abspath(path)+'/'+i,'rb').read()
        #img = toImage(img) #converter somente no recognition
        data.append(Request(i,img,f,imgType))
    return data'''

# read images from file
def readImage(path,f,imgType):
    data = []
    for cnt,i in enumerate(listdir(path)):
        if imgType == 1:
            img = cv2.imread(abspath(path)+'/'+i) 
        else:
            img = open(abspath(path)+'/'+i,'rb').read()
        
        data.append(requestService(i,img,f,imgType))
        #data.append(Request(i,img,f,1))
    return data

parse = argparse.ArgumentParser()
#parse.add_argument('modo',type=str,default='S',
#    help='S = Sobrepoe template') 
parse.add_argument('-dir',type=str,default='0',
    help= 'image folder')
parse.add_argument('-tipo',type=int,default='1',
    help= 'tipo = file type: 1-image | 2-base64')
parse.add_argument('-funcao',type=int,default='1', 
    help= 'functions available: 1-veriry person, 2-verify AND register, 3-register all')
args = parse.parse_args()

data = readImage(args.dir,args.tipo,args.funcao)
'''if (args.t ==1):
    data = readImage(args.dir,args.funcao)
else:
    data = readBase64(args.dir,args.funcao)'''
for i in data:
    main(i)
