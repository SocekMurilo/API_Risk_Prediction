# Windows
import os, sys

# Micro-Service
from flask import Flask, request, jsonify
from flask_cors import CORS

# Controller
import joblib
import pandas as pd
from matplotlib import pyplot as plt

# Modelo
from modelo_postgre import Machine_Learning

app = Flask(__name__)
CORS(app)

model = joblib.load('models/model.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        inputData = request.json

        Machine_Learning()

        typeRisk = inputData['Tipo de Risco']
        project = inputData['Projeto']
        metier = inputData['Metier']
        jalon = inputData['Jalon Afetado']
        probability = inputData['Probabilidade']
        impact = inputData['Impacto']
        plant = inputData['Planta']
        status = inputData['Status']

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

        return jsonify({'prediction': predictions_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)