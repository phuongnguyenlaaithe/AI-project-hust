from flask import Flask,request
from flask_cors import CORS
import helperFile as hf
import astar as algo
import conv_id
import astar2
import json

app = Flask(__name__)
CORS(app)

@app.route('/calculate', methods=['GET'])
def home():
    raw_input = request.args.get('pntdata').split(',')
    
    inputSourceLoc = (float(raw_input[0]),float(raw_input[1]))
    inputDestLoc = (float(raw_input[2]), float(raw_input[3]))

    mappedSourceLoc = hf.getKNN(inputSourceLoc)
    mappedDestLoc = hf.getKNN(inputDestLoc)

    print("Mapped Source Location:", mappedSourceLoc)
    print("Mapped Destination Location:", mappedDestLoc)

    # path = algo.aStar(mappedSourceLoc, mappedDestLoc)
    # finalPath, cost = hf.getResponsePathDict(path, mappedSourceLoc, mappedDestLoc)
    
    # thay the path
    path = astar2.astar(mappedSourceLoc, mappedDestLoc)
    finalPath = conv_id.convert_path(path)
    
    # print("Cost of the path(km): "+str(cost))
    return json.dumps(finalPath)

if __name__ == "__main__":
    app.run(host='0.0.0.0')