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

def readBase64(path,f):
    data = []
    for i in listdir(path):
        img = open(abspath(path)+'/'+i,'rb').read()
        img = toImage(img)
        data.append(Request(i,img,f))
    return data

def readImage(path,f):
    data = []
    for i in listdir(path):
        img = cv2.imread(abspath(path)+'/'+i) 
        data.append(Request(i,img,f))
    return data

parse = argparse.ArgumentParser()
#parse.add_argument('modo',type=str,default='S',
#    help='S = Sobrepoe template') 
parse.add_argument('dir',type=str,
    help= 'diretorio das imagens')
parse.add_argument('t',type=int, 
    help= 't = tipo de arquivo: 1-imagem | 2-base64')
parse.add_argument('funcao',type=int, 
    help= 'funcao a ser executada: 1-verifica pessoa, 2-verifica e cadastra novos, 3-cadastra todos')
args = parse.parse_args()

if (args.t ==1):
    data = readImage(args.dir,args.funcao)
else:
    data = readBase64(args.dir,args.funcao)

result = main(data)

for i in result:
    try:
        print(i[0])
    except:
        print(0)
        pass
