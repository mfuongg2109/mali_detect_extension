from flask import Flask, request, jsonify
from flask_cors import CORS
from Models.load_models import load_model, predict_all_model
from database import db, collection
from bson import ObjectId
from Extract_features.ExtractFeatures import getDomain
from Environment.path import *

app = Flask(__name__)
CORS(app)

@app.route("/check-url", methods=["POST"])
def check_url():
    data = request.get_json()
    url = data.get("url", "")
    domain = getDomain(url)

    document = collection.find_one({"domain": domain})

    if document:
        document["_id"] = str(document["_id"])

        # URL found in the database
        is_malicious = document["label"] == 1
        return jsonify({
            "url": url,
            "isMalicious": is_malicious,
            "details": document
        })
    else:
        is_malicious = predict_all_model(models, url)

        return jsonify({
            "url": url,
            "isMalicious": is_malicious,
            "message": "URL not found in the database"
        })

if __name__ == "__main__":
    model_path = [AdaBoost, DecisionTree, KNN, LDA, RandomForest]
    models = [load_model(path) for path in model_path]

    app.run(host = '0.0.0.0' , port = 5000)
