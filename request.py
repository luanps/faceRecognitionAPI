import sys
import argparse
from os import listdir
from os.path import isfile,join,abspath

class Request:
    def __init__(self,rn,company,log,device,app,lat,lon,keyPerson,attr,
        imgType,trueImage,truePC,img,pc,imgName):

        self.requestNumber = rn
        self.companyCode = company
        self.logCode = log
        self.captureDeviceCode = device

        #tipo de solicitacao
        self.appCode = app 

        self.latitude = lat
        self.longitude = lon
        self.keyPerson = keyPerson
        self.attrCode = attr
        self.typeImage = imgType
        self.trueImage = trueImage
        self.truePictureTree = truePC
        self.imageValidate = img
        self.validatePictureTree = pc

        self.imageName = imgName

        #self.companyCode,self.keyPerson,self.seqPerson = self.imageName.split('-')
        #self.seqPerson = self.seqPerson.split('.')[0]

        self.gender, self.birth, self.imgDate = self.imageName.split('-')[-3:]
        self.imgDate = self.imgDate.split('.')[0]

        self.idPerson = None

    #def getData(imageName):

    def isLatitude(self):
        try:
            if self.latitude < 90 and self.latitude> -90:
                return 1
        except:
            return 0

    def isLongitude(self):
        try:
            if self.longitude < 180 and self.longitude > -180:
                return 1
        except:
            return 0 


