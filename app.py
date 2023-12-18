#importing required libraries

from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
warnings.filterwarnings('ignore')
from feature import FeatureExtraction

file = open("pickle/model.pkl","rb")
gbc = pickle.load(file)
file.close()


app = Flask(__name__)

@app.route("/checkPhishing", methods=["POST"])
def index():
    data = request.get_json(force=True)
    url = data["url"]
    obj = FeatureExtraction(url)
    x = np.array(obj.getFeaturesList()).reshape(1,30) 
    y_pred =gbc.predict(x)[0]
    y_pro_phishing = gbc.predict_proba(x)[0,0]
    y_pro_non_phishing = gbc.predict_proba(x)[0,1]
    x = round(y_pro_non_phishing,2)
    num = x*100
    if (0<=x and x<0.50):
        num = 100-num
    if(x<=1 and x>=0.50): 
        return jsonify({"isMalicious": False})
    if(0<=x and x<0.50): 
         return jsonify({"isMalicious": True})

if __name__ == "__main__":
    app.run(debug=True)