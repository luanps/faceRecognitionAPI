'''Recognition functions - Server side.
The face detection, alignment and recognition models are obtained
from dlib.net
'''
import cv2
import dlib
import sys
import os
import glob
import numpy as np
import _pickle as cPickle
import mysql.connector
import base64
import codecs
import time
import json
from returnFile import Return

#instantiate face detector,alignment and recogntion from Dlib
predictor = 'model2.dat'
face_rec = 'model1.dat'
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor)
facerec = dlib.face_recognition_model_v1(face_rec)

#Define a recogntion threshold
THRESH = .2#0.1 #0.5

#Convert RGB image to Base64
def toBase64(f):
    retval, b64 = cv2.imencode('.jpg', f)
    return  base64.b64encode(b64) 

#Convert base64 image to RGB
def toImage(f):
    #b64 = base64.b64decode(f[1:-1])

    if ',' in f:
        f = f.split(',')[-1]
        
    b64 = base64.b64decode(f)
    b64 = np.frombuffer(b64,dtype = np.uint8)
    img = cv2.imdecode(b64,flags=1)
    return img
    #dec = np.fromstring(codecs.decode(f,'base64'), np.uint8)
    #return cv2.imdecode(dec, cv2.IMREAD_ANYCOLOR)

#Connect to database
def connectDB():
    cnx = mysql.connector.connect(user='root',
        password='123456',host='localhost',database='db')
    cursor = cnx.cursor(buffered=True)
    return [cnx,cursor] 


#Face detection, alignment and feature extraction
#detecta face e extrai vetor de caracteristicas
def extractFeatures(image):
    dets = detector(image, 1)
    d = dets[0]
    shape = sp(image, d)
    feat = facerec.compute_face_descriptor(image, shape)
    #bb = [d.top(),d.bottom(),d.left(),d.right()]
    bb = [d.left(),d.top(),d.right(),d.bottom()]
    #face_crop = img[d.top():d.bottom(),d.left():d.right()]
    return (np.asarray(feat),bb,shape)


#Verify if Company is registered on the database by companyCode
#verifica se empresa esta cadastrada
def isCustomer(data):
    conn[1].execute("select id from empresa;")
    idCompany = conn[1].fetchall()
    if (int(data.companyCode) in [x[0] for x in idCompany]):
        return 1
    return 0

#1:n face recognition query on the database, comparing its 128-dim facial features
#consulta 1 para n na base de dados
def verify(data):
    try:
        feat,bb,shape = extractFeatures(data.imageValidate)
    except BaseException:
       return -1
    #recupera dados da base e compara
    conn[1].execute( """ select chave,pessoa.id, 
        POW(tpl001-%s,2) + POW(tpl002-%s,2) + POW(tpl003-%s,2) + POW(tpl004-%s,2) + 
        POW(tpl005-%s,2) + POW(tpl006-%s,2) + POW(tpl007-%s,2) + POW(tpl008-%s,2) + 
        POW(tpl009-%s,2) + POW(tpl010-%s,2) + POW(tpl011-%s,2) + POW(tpl012-%s,2) + 
        POW(tpl013-%s,2) + POW(tpl014-%s,2) + POW(tpl015-%s,2) + POW(tpl016-%s,2) + 
        POW(tpl017-%s,2) + POW(tpl018-%s,2) + POW(tpl019-%s,2) + POW(tpl020-%s,2) + 
        POW(tpl021-%s,2) + POW(tpl022-%s,2) + POW(tpl023-%s,2) + POW(tpl024-%s,2) + 
        POW(tpl025-%s,2) + POW(tpl026-%s,2) + POW(tpl027-%s,2) + POW(tpl028-%s,2) + 
        POW(tpl029-%s,2) + POW(tpl030-%s,2) + POW(tpl031-%s,2) + POW(tpl032-%s,2) + 
        POW(tpl033-%s,2) + POW(tpl034-%s,2) + POW(tpl035-%s,2) + POW(tpl036-%s,2) + 
        POW(tpl037-%s,2) + POW(tpl038-%s,2) + POW(tpl039-%s,2) + POW(tpl040-%s,2) + 
        POW(tpl041-%s,2) + POW(tpl042-%s,2) + POW(tpl043-%s,2) + POW(tpl044-%s,2) + 
        POW(tpl045-%s,2) + POW(tpl046-%s,2) + POW(tpl047-%s,2) + POW(tpl048-%s,2) + 
        POW(tpl049-%s,2) + POW(tpl050-%s,2) + POW(tpl051-%s,2) + POW(tpl052-%s,2) + 
        POW(tpl053-%s,2) + POW(tpl054-%s,2) + POW(tpl055-%s,2) + POW(tpl056-%s,2) + 
        POW(tpl057-%s,2) + POW(tpl058-%s,2) + POW(tpl059-%s,2) + POW(tpl060-%s,2) + 
        POW(tpl061-%s,2) + POW(tpl062-%s,2) + POW(tpl063-%s,2) + POW(tpl064-%s,2) + 
        POW(tpl065-%s,2) + POW(tpl066-%s,2) + POW(tpl067-%s,2) + POW(tpl068-%s,2) + 
        POW(tpl069-%s,2) + POW(tpl070-%s,2) + POW(tpl071-%s,2) + POW(tpl072-%s,2) + 
        POW(tpl073-%s,2) + POW(tpl074-%s,2) + POW(tpl075-%s,2) + POW(tpl076-%s,2) + 
        POW(tpl077-%s,2) + POW(tpl078-%s,2) + POW(tpl079-%s,2) + POW(tpl080-%s,2) + 
        POW(tpl081-%s,2) + POW(tpl082-%s,2) + POW(tpl083-%s,2) + POW(tpl084-%s,2) + 
        POW(tpl085-%s,2) + POW(tpl086-%s,2) + POW(tpl087-%s,2) + POW(tpl088-%s,2) + 
        POW(tpl089-%s,2) + POW(tpl090-%s,2) + POW(tpl091-%s,2) + POW(tpl092-%s,2) + 
        POW(tpl093-%s,2) + POW(tpl094-%s,2) + POW(tpl095-%s,2) + POW(tpl096-%s,2) + 
        POW(tpl097-%s,2) + POW(tpl098-%s,2) + POW(tpl099-%s,2) + POW(tpl100-%s,2) + 
        POW(tpl101-%s,2) + POW(tpl102-%s,2) + POW(tpl103-%s,2) + POW(tpl104-%s,2) + 
        POW(tpl105-%s,2) + POW(tpl106-%s,2) + POW(tpl107-%s,2) + POW(tpl108-%s,2) + 
        POW(tpl109-%s,2) + POW(tpl110-%s,2) + POW(tpl111-%s,2) + POW(tpl112-%s,2) + 
        POW(tpl113-%s,2) + POW(tpl114-%s,2) + POW(tpl115-%s,2) + POW(tpl116-%s,2) + 
        POW(tpl117-%s,2) + POW(tpl118-%s,2) + POW(tpl119-%s,2) + POW(tpl120-%s,2) + 
        POW(tpl121-%s,2) + POW(tpl122-%s,2) + POW(tpl123-%s,2) + POW(tpl124-%s,2) + 
        POW(tpl125-%s,2) + POW(tpl126-%s,2) + POW(tpl127-%s,2) + POW(tpl128-%s,2) 
        AS square_dist from pessoa_empresa,pessoa
        where pessoa.id=pessoa_empresa.id_pessoa 
        AND pessoa_empresa.id_empresa=%s %s %s %s """
        %(float(feat[0]),
        float(feat[1]), float(feat[2]), float(feat[3]), float(feat[4]),
        float(feat[5]), float(feat[6]), float(feat[7]), float(feat[8]),
        float(feat[9]), float(feat[10]), float(feat[11]), float(feat[12]),
        float(feat[13]), float(feat[14]), float(feat[15]), float(feat[16]),
        float(feat[17]), float(feat[18]), float(feat[19]), float(feat[20]),
        float(feat[21]), float(feat[22]), float(feat[23]), float(feat[24]),
        float(feat[25]), float(feat[26]), float(feat[27]), float(feat[28]),
        float(feat[29]), float(feat[30]), float(feat[31]), float(feat[32]),
        float(feat[33]), float(feat[34]), float(feat[35]), float(feat[36]),
        float(feat[37]), float(feat[38]), float(feat[39]), float(feat[40]),
        float(feat[41]), float(feat[42]), float(feat[43]), float(feat[44]),
        float(feat[45]), float(feat[46]), float(feat[47]), float(feat[48]),
        float(feat[49]), float(feat[50]), float(feat[51]), float(feat[52]),
        float(feat[53]), float(feat[54]), float(feat[55]), float(feat[56]),
        float(feat[57]), float(feat[58]), float(feat[59]), float(feat[60]),
        float(feat[61]), float(feat[62]), float(feat[63]), float(feat[64]),
        float(feat[65]), float(feat[66]), float(feat[67]), float(feat[68]),
        float(feat[69]), float(feat[70]), float(feat[71]), float(feat[72]),
        float(feat[73]), float(feat[74]), float(feat[75]), float(feat[76]),
        float(feat[77]), float(feat[78]), float(feat[79]), float(feat[80]),
        float(feat[81]), float(feat[82]), float(feat[83]), float(feat[84]),
        float(feat[85]), float(feat[86]), float(feat[87]), float(feat[88]),
        float(feat[89]), float(feat[90]), float(feat[91]), float(feat[92]),
        float(feat[93]), float(feat[94]), float(feat[95]), float(feat[96]),
        float(feat[97]), float(feat[98]), float(feat[99]), float(feat[100]),
        float(feat[101]), float(feat[102]), float(feat[103]), float(feat[104]),
        float(feat[105]), float(feat[106]), float(feat[107]), float(feat[108]),
        float(feat[109]), float(feat[110]), float(feat[111]), float(feat[112]),
        float(feat[113]), float(feat[114]), float(feat[115]), float(feat[116]),
        float(feat[117]), float(feat[118]), float(feat[119]), float(feat[120]),
        float(feat[121]), float(feat[122]), float(feat[123]), float(feat[124]),
        float(feat[125]), float(feat[126]), float(feat[127]),
        data.companyCode, 'ORDER BY', 'square_dist', 'ASC LIMIT 1'))

    resQuery = conn[1].fetchall()
    if resQuery:
        if resQuery[0][-1] < THRESH:
            #return (resQuery[0],feat,bb,shape)
            data.idPerson = resQuery[0][1] 
            #return (data.idPerson,resQuery[0][0]) #retorna pessoa.id e chave
            return (resQuery[0][0]) #retorna pessoa.id e chave
    #pessoa nao encontrada - not found on the database
    return 0
    
#Get the last ID registered on the database table
def lastid(table):
    conn[1].execute('select id from %s order by id desc limit 1'%table)
    lastId =  conn[1].fetchone()
    return 1 if lastId is None else  (int(lastId[0])+1)

#insert a new person on Company's database
#insere pessoa na base de dados da empresa
def register(data):

    try:
        feat,bb,shape = extractFeatures(data.imageValidate)
    except BaseException:
       return -1

    data.idPerson = lastid('pessoa')
    conn[1].execute("""insert into pessoa (id) values (%s)""",(data.idPerson,))

    '''conn[1].execute("""insert into pessoa_atributo (id_pessoa,dt_captura,id_dispositivo,
        latitude,longitude) values (%s,%s,%s,%s,%s)""",(idPerson,getDatetime,data.captureDeviceCode,
        data.latitude,data.longitude))'''

    dt = str(time.strftime('%Y-%m-%d %H:%M:%S'))
    conn[1].execute("""insert into pessoa_empresa (id_empresa,id_pessoa,chave,dt_criou, id_dispositivo,
        latitude_criou,longitude_criou) values (%s,%s,%s,%s,%s,%s,%s)""", (int(data.companyCode),
        data.idPerson,str(data.keyPerson),dt,data.captureDeviceCode,data.latitude, data.longitude))

    for i in range(1,129):
        conn[1].execute("""update pessoa set tpl{:03} = %s where id=%s; """.format(i)
            %(feat[i-1],data.idPerson))

    '''for i in range(1,129):
        if i==1:
            conn[1].execute("""insert into pessoa_template (id,f%d) values (%s,%s);"""
                %(i,data.idPersonTemplate,feat[i-1]))
        else:
            conn[1].execute("""update pessoa_template set f%d = %s where id=%s; """
                %(i,feat[i-1],idPersonTemplate))
    conn[1].execute("""insert into pessoa (id,id_pessoa_template) values (%s,%s)""",
        (idPerson,idPersonTemplate))
    conn[1].execute("""insert into pessoa_empresa (id_empresa,id_pessoa,chave)
         values (%s,%s,%s); """,(int(data.companyCode),idPerson,str(data.keyPerson)))'''

    conn[0].commit() #salva alteracoes no bd - save updates on database
    return data.idPerson

    #lastId = conn[1].lastrowid #ultimo id consultado pelo conn

#check if Device exists on given Company
#verifica se dispositivo existe na empresa
def isDevice(data):
    
    #check if deviceCode exists:
    conn[1].execute('select id from dispositivo') 
    getData = conn[1].fetchall()
    if (int(data.captureDeviceCode) not in [x[0] for x in getData]):
        return 5012
    
    #check if deviceCode belongs to a sector
    conn[1].execute("""select dispositivo.id from dispositivo,setor where dispositivo.id=%s and 
        dispositivo.id_setor = setor.id"""%data.captureDeviceCode) 
    getData = conn[1].fetchall()
    if (int(data.captureDeviceCode) not in [x[0] for x in getData]):
        return 5002 #revisar este codigo de erro

    #check if sector belongs to company:
    conn[1].execute("""select dispositivo.id from dispositivo,setor,empresa where dispositivo.id=%s and 
        dispositivo.id_setor = setor.id and setor.id_empresa=%s"""%(data.captureDeviceCode,data.companyCode))
    getData = conn[1].fetchall()
    if (int(data.captureDeviceCode) not in [x[0] for x in getData]):
        return 5002 #revisar este codigo de erro

    return 0

#check if request code is valid (need to be an option between 1 and 4)
def isAppCode(data):
    if int(data.appCode) in range(1,4):
        return 1
    return 0

#insert data on pessoa_log table
def genLog(data):
    dt = str(time.strftime('%Y-%m-%d %H:%M:%S'))
    img = toBase64(data.imageValidate)
    #conn[1].execute("""insert into pessoa_log (id_pessoa,dt_log,id_dispositivo,latitude,longitude,foto)
    #         values (%s,%s,%s,%s,%s,%s)""",(data.idPerson,dt,data.captureDeviceCode,data.latitude,data.longitude,img))
    conn[1].execute("""insert into pessoa_log (id_pessoa,dt_log,id_dispositivo,latitude,longitude)
         values (%s,%s,%s,%s,%s)""",(data.idPerson,dt,data.captureDeviceCode,data.latitude,data.longitude))
    conn[0].commit() #salva alteracoes no bd
    return

#Check if latitute format is correct
def isLatitude(data):
    try:
        if float(data.latitude) < 90 and float(data.latitude) > -90:
            return 0
    except:
        return 1
    return 1

#Check if longitude format is correct
def isLongitude(data):
    try:
        if float(data.longitude) < 180 and float(data.longitude) > -180:
            return 0
    except:
        return 1
    return 1

#cod 1 verifica pessoa na base da empresa, retorna codigo dela
#cod 2 verifica pessoa na base da empresa, se nao existir CADASTRE
#cod 3 cadastre pessoa na base da empresa

def runRecognition(d):
    status = 0
    #OBS.: falta validar o codigo do log aqui

    if not isCustomer(d):
        return 5005,-1 #5002?

    #verifica se dispositivo existe FALTA TESTAR
    device = isDevice(d)
    if device:
        return device,-1

    if not isAppCode(d):
        return  5001,-1
    
    if isLongitude(d):
        return  5013,-1

    if isLatitude(d):
        return 5014,-1
   
    #verifica e converte base64 para imagem 
    #falta testar
    if int(d.typeImage) == 2:
        try:
            d.imageValidate = toImage(d.imageValidate)  
            
        except:
            return 5009,-1
            
    #1:n face verification on company's database
    if int(d.appCode) == 1:

        resultQuery = verify(d)
        #face detection failed, return incompatible image error
        if resultQuery ==-1:
            return 5009,-1
        #person not found
        if not resultQuery:
            status = 3
        else:
            #person found
            status = 1

    #1:n face verification on company's databse AND register it if not encountered
    elif int(d.appCode) == 2:

        resultQuery =  verify(d)
        #face detection failed, return incompatible image error
        if resultQuery == -1:
            return 5009,-1
        #person not found
        if not resultQuery:
            #insert person on database
            resultQuery = register(d)
            if resultQuery == -1:
                return 5009,-1
            status = 6

        #person not found, do not insert it to databse
        else:
            status = 1

    #cadastra na base da empresa
    elif int(d.appCode) == 3:
        resultQuery = register(d)
        if resultQuery == -1:
            return 5009,-1
        status = 6

    #insere na tabela pessoa_log se cadastro for realizado ou pessoa encontrada 
    if status < 5000 and resultQuery!=0 and resultQuery!=-1:
        genLog(d)
    return ([status,resultQuery]) 

#main function, receives a JSON data, unpack it and run recognition functions
# it returns a JSON output file
def main(data):
    global conn
    conn = connectDB()
    status = runRecognition(data)
    if len(status)>1 and status[1]!=0 and status[1]!=-1:
        jsFile = json.dumps(Return(data.requestNumber,
                status[0],status[1],data.keyPerson).__dict__)
    else:
        jsFile = json.dumps(Return(data.requestNumber,status[0],
                999999999,data.keyPerson).__dict__)
    #d.requestNumber , status, pessoa.id (senao retorna '999999999'
    conn[1].close()
    conn[0].close()
    return jsFile
