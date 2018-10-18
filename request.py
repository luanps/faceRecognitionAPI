import sys
import argparse
from os import listdir
from os.path import isfile,join,abspath

class Request:
    def __init__(self,rn,company,log,device,app,lat,lon,keyPerson,attr,
        imgType,trueImage,truePC,img,pc,free):

        self.requestNumber = rn
        self.companyCode = company
        self.logCode = log
        self.captureDeviceCode = device
        self.appCode = app #tipo de solicitacao
        self.latitude = lat
        self.longitude = lon
        self.keyPerson = keyPerson
        self.attrCode = attr
        self.typeImage = imgType
        self.trueImage = trueImage
        self.truePictureTree = truePC
        self.imageValidate = img
        self.validatePictureTree = pc
        self.free = free

        #self.imageName = imgName
        #self.companyCode,self.keyPerson,self.seqPerson = self.imageName.split('-')
        #self.seqPerson = self.seqPerson.split('.')[0]

   def isLat(self.lat):
       try:
           if self.lat < 90 and self.lat> -90:
               return 1
       except:
        return 0

   def isLon(self.lon):
        try:
            if self.lon < 180 and self.lon > -180:
                return 1
        except:
            return 0 


