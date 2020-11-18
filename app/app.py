from flask import Flask
from flask import render_template
from flask import request
import json
import datasampling as datSamp
import pca
import mds

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# get data sample
@app.route("/getData", methods=['POST'])
def getData():
    datSamp.importData("finalData.csv")
    
    pointsToKeep = request.json['pointsToKeep']
    maximumK = request.json['maximumK']
    elbowAngleRatio = request.json['elbowAngleRatio']

    output = dict()
    output['stratified'] = datSamp.stratifiedSampling(datSamp.initial_data, pointsToKeep, maximumK, elbowAngleRatio)
    output['attributes'] = datSamp.attributes
    
    return json.dumps(output)

# get PCA data
@app.route("/getPCAData", methods=['POST'])
def getPCAData():
    print("Running PCA...")
    data = request.json['data']
    attributes = request.json['attributes']

    output = pca.getPCAStuff(data, attributes)

    return json.dumps(output)

# get MDS data
@app.route("/getMDSData", methods=['POST'])
def getMDSData():
    print("Running MDS...")
    data = request.json['data']
    attributes = request.json['attributes']

    output = mds.getMDSStuff(data, attributes)

    return json.dumps(output)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)