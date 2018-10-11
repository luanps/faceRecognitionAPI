import pdb
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
predictor = 'model2.dat'
face_rec = 'model1.dat'
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor)
facerec = dlib.face_recognition_model_v1(face_rec)
THRESH = .2#0.1 #0.5

def toBase64(f):
    return  base64.b64encode(f) 

def toImage(f): 
    dec = np.fromstring(codecs.decode(f,'base64'), np.uint8)
    return cv2.imdecode(dec, cv2.IMREAD_ANYCOLOR)

def connectDB():
    cnx = mysql.connector.connect(user='root',
        password='mimago',host='localhost',database='imc')
    cursor = cnx.cursor(buffered=True)
    return [cnx,cursor] 

#verifica se empresa esta cadastrada
def isCustomer(data):
    conn[1].execute("select id from empresa;")
    idCompany = conn[1].fetchall()
    if (int(data.companyCode) in [x[0] for x in idCompany]):
        return 1
    return 0


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

#consulta 1 para n na base de dados
def verify(data):
    try:
        feat,bb,shape = extractFeatures(data.imageValidate)
    except BaseException:
       return 0
    #recupera dados da base e compara
    conn[1].execute( """ select chave,pessoa.id, 
        POW(f1-%s,2) + POW(f2-%s,2) + POW(f3-%s,2) + POW(f4-%s,2) + 
        POW(f5-%s,2) + POW(f6-%s,2) + POW(f7-%s,2) + POW(f8-%s,2) + 
        POW(f9-%s,2) + POW(f10-%s,2) + POW(f11-%s,2) + POW(f12-%s,2) + 
        POW(f13-%s,2) + POW(f14-%s,2) + POW(f15-%s,2) + POW(f16-%s,2) + 
        POW(f17-%s,2) + POW(f18-%s,2) + POW(f19-%s,2) + POW(f20-%s,2) + 
        POW(f21-%s,2) + POW(f22-%s,2) + POW(f23-%s,2) + POW(f24-%s,2) + 
        POW(f25-%s,2) + POW(f26-%s,2) + POW(f27-%s,2) + POW(f28-%s,2) + 
        POW(f29-%s,2) + POW(f30-%s,2) + POW(f31-%s,2) + POW(f32-%s,2) + 
        POW(f33-%s,2) + POW(f34-%s,2) + POW(f35-%s,2) + POW(f36-%s,2) + 
        POW(f37-%s,2) + POW(f38-%s,2) + POW(f39-%s,2) + POW(f40-%s,2) + 
        POW(f41-%s,2) + POW(f42-%s,2) + POW(f43-%s,2) + POW(f44-%s,2) + 
        POW(f45-%s,2) + POW(f46-%s,2) + POW(f47-%s,2) + POW(f48-%s,2) + 
        POW(f49-%s,2) + POW(f50-%s,2) + POW(f51-%s,2) + POW(f52-%s,2) + 
        POW(f53-%s,2) + POW(f54-%s,2) + POW(f55-%s,2) + POW(f56-%s,2) + 
        POW(f57-%s,2) + POW(f58-%s,2) + POW(f59-%s,2) + POW(f60-%s,2) + 
        POW(f61-%s,2) + POW(f62-%s,2) + POW(f63-%s,2) + POW(f64-%s,2) + 
        POW(f65-%s,2) + POW(f66-%s,2) + POW(f67-%s,2) + POW(f68-%s,2) + 
        POW(f69-%s,2) + POW(f70-%s,2) + POW(f71-%s,2) + POW(f72-%s,2) + 
        POW(f73-%s,2) + POW(f74-%s,2) + POW(f75-%s,2) + POW(f76-%s,2) + 
        POW(f77-%s,2) + POW(f78-%s,2) + POW(f79-%s,2) + POW(f80-%s,2) + 
        POW(f81-%s,2) + POW(f82-%s,2) + POW(f83-%s,2) + POW(f84-%s,2) + 
        POW(f85-%s,2) + POW(f86-%s,2) + POW(f87-%s,2) + POW(f88-%s,2) + 
        POW(f89-%s,2) + POW(f90-%s,2) + POW(f91-%s,2) + POW(f92-%s,2) + 
        POW(f93-%s,2) + POW(f94-%s,2) + POW(f95-%s,2) + POW(f96-%s,2) + 
        POW(f97-%s,2) + POW(f98-%s,2) + POW(f99-%s,2) + POW(f100-%s,2) + 
        POW(f101-%s,2) + POW(f102-%s,2) + POW(f103-%s,2) + POW(f104-%s,2) + 
        POW(f105-%s,2) + POW(f106-%s,2) + POW(f107-%s,2) + POW(f108-%s,2) + 
        POW(f109-%s,2) + POW(f110-%s,2) + POW(f111-%s,2) + POW(f112-%s,2) + 
        POW(f113-%s,2) + POW(f114-%s,2) + POW(f115-%s,2) + POW(f116-%s,2) + 
        POW(f117-%s,2) + POW(f118-%s,2) + POW(f119-%s,2) + POW(f120-%s,2) + 
        POW(f121-%s,2) + POW(f122-%s,2) + POW(f123-%s,2) + POW(f124-%s,2) + 
        POW(f125-%s,2) + POW(f126-%s,2) + POW(f127-%s,2) + POW(f128-%s,2)
        AS square_dist from pessoa_empresa,pessoa,pessoa_template
        where pessoa.id=pessoa_empresa.id_pessoa 
        AND  pessoa.id_pessoa_template = pessoa_template.id AND 
        pessoa_empresa.id_empresa=%s %s %s %s """
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
            return (resQuery[0],feat,bb,shape)
    return 0
    

def lastid(table):
    conn[1].execute('select id from %s order by id desc limit 1'%table)
    lastId =  conn[1].fetchone()
    return 1 if lastId is None else  (int(lastId[0])+1)

#insere pessoa na base de dados da empresa
def register(data):

    try:
        feat,bb,shape = extractFeatures(data.imageValidate)
    except BaseException:
       return 

    idPerson = lastid('pessoa')
    idPersonTemplate = lastid('pessoa_template')

    for i in range(1,129):
        if i==1:
            conn[1].execute("""insert into pessoa_template (id,f%d) values (%s,%s);"""
                %(i,idPersonTemplate,feat[i-1]))
        else:
            conn[1].execute("""update pessoa_template set f%d = %s where id=%s; """
                %(i,feat[i-1],idPersonTemplate))
    conn[1].execute("""insert into pessoa (id,id_pessoa_template) values (%s,%s)""",
        (idPerson,idPersonTemplate))
    conn[1].execute("""insert into pessoa_empresa (id_empresa,id_pessoa,chave)
         values (%s,%s,%s); """,(int(data.companyCode),idPerson,str(data.keyPerson)))
    conn[0].commit()

    #lastId = conn[1].lastrowid #ultimo id consultado pelo conn


#cod 1 verifica pessoa na base da empresa, retorna codigo dela
#cod 2 verifica pessoa na base da empresa, se nao existir CADASTRE
#cod 3 cadastre pessoa na base da empresa

def main(data):
    global conn
    conn = connectDB()
    result = [] 
    for d in data:
       
        # verifica se empresa esta cadastrada 
        if not isCustomer(d):
            result.append(5005) 
            continue 

        #verifica 1-n na base da empresa
        if d.appCode == 1:
            result.append(verify(d))

        #verifica 1-n na base da empresa E cadastra
        elif d.appCode == 2:
            verifyPerson =  verify(d)
            if not verifyPerson:
                result.append(register(d))
            else:
                result.append(verifyPerson)

        #cadastra na base da empresa
        elif d.appCode == 3:
            result.append(register(d))
        else:
            continue
    conn[1].close()
    conn[0].close()
    return result 
