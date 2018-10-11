import sys
import argparse
from os import listdir
from os.path import isfile,join,abspath

class Request:
    def __init__(self,imageName,img,appCode):

        self.requestNumber = None 
        self.logCode = None
        self.captureDeviceCode = None
        self.appCode = appCode
        self.latitude = None
        self.longitude = None
        self.attrCode = None
        self.typeImage = 1
        self.trueImage = None
        self.truePictureTree = None
        self.imageValidate = img	

        self.imageName = imageName
        self.companyCode,self.keyPerson,self.seqPerson = self.imageName.split('-')
        self.seqPerson = self.seqPerson.split('.')[0]

        #out of service
        self.sexo = None
        self.dtNascimento = None
        self.dtCaptura = None
    



