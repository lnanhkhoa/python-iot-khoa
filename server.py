####        IMPORT      ####
import os, json
from flask import Flask
from flask import render_template
from flask import request,redirect
import time
import ibmiotf.application

####    INFO of device      ####
deviceType = "raspberrypi"
deviceId = "b827eb217087"

####    Bien dung cho hien thi ket qua tren WebApp gui tu iotf-service    ####
strLed1 = 'None'
strLed2 = 'None'

####    Code xac thuc truyen + nhan cua iotf-service    ####
vcap = json.loads(os.getenv("VCAP_SERVICES"))
try:
    options = {
    "org": vcap["iotf-service"][0]["credentials"]["org"],
    "id": vcap["iotf-service"][0]["credentials"]["iotCredentialsIdentifier"],
    "auth-method": "apikey",
    "auth-key": vcap["iotf-service"][0]["credentials"]["apiKey"],
    "auth-token": vcap["iotf-service"][0]["credentials"]["apiToken"]
    }
    appcli = ibmiotf.application.Client(options)
    appcli.connect()
except ibmiotf.ConnectionException as e:
    print e
####    Chuong trinh chinh      ####
app = Flask(__name__)

if os.getenv("VCAP_APP_PORT"):
    port = int(os.getenv("VCAP_APP_PORT"))
else:
    port = 8080

####    Function thuc hien cac lenh truyen thong tin service den iotf nham muc dich control device
@app.route('/')
def hello():
    return render_template('index.html', statusLed1='None', statusLed2='None')

@app.route('/led1/<command>', methods=['GET','POST'])
def led1_route(command):
    global strLed1
    global strLed2
    myData = {'command' : command}
    strLed1 = 'send '+ command
    strLed2 = 'None'
    appcli.publishEvent("raspberrypi", deviceId, "led1", "json", myData)
    return render_template('index.html', statusLed1=strLed1, statusLed2=strLed2)

@app.route('/led2/<command>', methods=['GET','POST'])
def led2_route(command):
    global strLed1
    global strLed2
    myData = {'command' : command}
    strLed1 = 'None'
    strLed2 = 'send '+ command
    appcli.publishEvent("raspberrypi", deviceId, "led2", "json", myData)
    return render_template('index.html',statusLed1=strLed1, statusLed2=strLed2)

####    Main   ####
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=port)