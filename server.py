from flask import Flask,request,jsonify
import json
from recognition import main
import logging
from collections import namedtuple
from recordtype import recordtype
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def getRequest():
    jdata = request.get_json()
    data = json.loads(jdata)    
    #data = (namedtuple("Request",data.keys())(*data.values()))
    data = (recordtype("Request",data.keys())(*data.values()))
    res = main(data)
    res = json.dumps(res)
    return res

if __name__ == '__main__':
    app.run(debug=True)
