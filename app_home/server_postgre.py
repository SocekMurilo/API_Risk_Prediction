# Windows
import os, sys

# Micro-Service
from flask import Flask, request, jsonify
from flask_cors import CORS

# Controller
import joblib
import pandas as pd
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

# Modelo
from models.modelo_postgre import Machine_Learning

app = Flask(__name__)
CORS(app)

model = joblib.load('models/model.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        inputData = request.json

        Machine_Learning()

        typeRisk = inputData['rskType']
        project = inputData['rskProjectId']
        metier = inputData['rskMetier']
        jalon = inputData['rskJalon']
        probability = inputData['rskProbability']
        impact = inputData['rskImpact']
        plant = inputData['rskPlant']
        status = inputData['rskStatus']

        data = pd.DataFrame({
                "rsk_type": [typeRisk],
                "rsk_probability": [probability],
                "rsk_project_id": [project],
                "rsk_impact": [impact],
                "rsk_plant" : [plant],
                "rsk_jalon": [jalon],
                "rsk_metier": [metier],
                "rsk_status": [status]
        })


        print("Colunas do new_data:", data.columns)

        predictions = model.predict(data)
        predictions_list = predictions.tolist()

        return jsonify({'rskClassification': predictions_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5020)
    print(" * Running on http://0.0.0.0:5020")