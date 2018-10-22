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

#cria solicitacao de servico para a imagem passada como parametro e demais dados de exemplo:
def requestService(imgName,img,appCode,imgType): 

    #request number random
    rn = random.randint(1,1000000)
    #log number random
    log = random.randint(1,1000000)

    #device de testes = 123 (insere empresa 1 )
    #device de testes DETRAN = 1 (insere empresa 3)
    device = 1

    #coordenadas imago
    lat = -25.450 
    lon = -49.231 
    #dados nome da imagem
    company,keyPerson,seqPerson = imgName.split('-')[:3]
    #atributo
    attr = 0
    #imagem verdadeira default=99
    trueImage = 99
    #point cloud verdadeiro default=99
    truePC = 99
    #point cloud validar default=99
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

def readImage(path,f,imgType):
    data = []
    for cnt,i in enumerate(listdir(path)):
        #if cnt>320: #XUNXO PULA N PRIMEiROS
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
    help= 'diretorio das imagens')
parse.add_argument('-tipo',type=int,default='1',
    help= 'tipo = tipo de arquivo: 1-imagem | 2-base64')
parse.add_argument('-funcao',type=int,default='1', 
    help= 'funcao a ser executada: 1-verifica pessoa, 2-verifica e cadastra novos, 3-cadastra todos')
args = parse.parse_args()

data = readImage(args.dir,args.tipo,args.funcao)
'''if (args.t ==1):
    data = readImage(args.dir,args.funcao)
else:
    data = readBase64(args.dir,args.funcao)'''
for i in data:
    main(i)
