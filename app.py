from flask import Flask, render_template, request, jsonify, redirect, jsonify, url_for, redirect, send_from_directory
import numpy as np
import pickle
import cv2
from PIL import Image
import warnings
warnings.simplefilter("ignore", DeprecationWarning)

app = Flask(__name__)
model_svc = pickle.load(open('./models/svc_model',"rb"))
model_knc = pickle.load(open('./models/KNeighborsClassifier_model','rb'))
model_bc = pickle.load(open('./models/BaggingClassifier_model','rb'))
model_rfc = pickle.load(open('./models/RandomForestClassifier_model','rb'))
model_dtc = pickle.load(open('./models/DecisionTreeClassifier_model','rb'))
model_etc = pickle.load(open('./models/ExtraTreeClassifier_model',"rb"))
model_gnb = pickle.load(open('./models/GaussianNB_model','rb'))
model_gbc = pickle.load(open('./models/GradienBoostingClassifier_model','rb'))
model_lr = pickle.load(open('./models/LogisticRegression_model','rb'))
model_sgdc = pickle.load(open('./models/SGDClassifier_model','rb'))
alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

def preprocessImage(img):
    im = img
    im_gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    im_gray =cv2.GaussianBlur(im_gray,(15,15),0)
    roi = cv2.resize(im_gray,(28,28), interpolation=cv2.INTER_AREA)
    rows,cols = roi.shape
    data = []
    for i in range(rows):
        for j in range(cols):
            data.append(roi[i,j]) 
    r_im = np.asarray(data)
    r_im = r_im.reshape(1,-1)
    return r_im

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html', errorM = 'fade')

@app.route('/',methods=['POST'])
def recognize():
    file = request.files['image'].read()
    if(file):
        npimg = np.fromstring(file, np.uint8)
        img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
        data = preprocessImage(img)
        psvc = model_svc.predict(data)
        pknc = model_knc.predict(data)
        pbc = model_bc.predict(data)
        pdtc = model_dtc.predict(data)
        prfc = model_rfc.predict(data)
        petc = model_etc.predict(data)
        pgnb = model_gnb.predict(data)
        pgbc = model_gbc.predict(data)
        plr = model_lr.predict(data)
        psgdc = model_sgdc.predict(data)
        asvc = alphabet[psvc[0]]
        aknc = alphabet[pknc[0]]
        abc = alphabet[pbc[0]]
        adtc = alphabet[pdtc[0]]
        arfc = alphabet[prfc[0]]
        aetc = alphabet[petc[0]]
        agnb = alphabet[pgnb[0]]
        agbc = alphabet[pgbc[0]]
        alr = alphabet[plr[0]]
        asgdc = alphabet[psgdc[0]]
        prediction = [["SVC",asvc],["KNeigborsClassifier",aknc],["BaggingClassifier",abc],["DecisionTreeClassifier",adtc],["RandomForestClassifier",arfc],
        ["ExtraTreeClassifier",aetc],["GaussianNB",agnb],["GradienBoostingClassifier",agbc],["LogisticRegression",alr],["SGDClassifier",asgdc]]
        return render_template('index.html', show = 'show',errorM = 'fade' , prediction = prediction)
    else:
        return render_template('index.html',show = "", errorM = "")

if __name__ == '__main__':
    app.run(debug=True)