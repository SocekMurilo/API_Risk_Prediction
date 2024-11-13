# Micro-Service
from flask import Flask, request, jsonify
from flask_cors import CORS

# Controller
import joblib
import pandas as pd
from matplotlib import pyplot as plt

# from training_Excel import Machine_Learning
from modelo_postgre import Machine_Learning


##########################################################################

app = Flask(__name__)
CORS(app)

model = joblib.load('models/model.joblib')
# preprocessor = joblib.load('models/preprocessor.joblib')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        inputData = request.json

        typeRisk = inputData['Tipo de Risco']
        impact_Consequence = inputData['Impacto/Consequencia']
        project = inputData['Projeto']
        metier = inputData['Metier']
        jalon = inputData['Jalon Afetado']
        probability = inputData['Probabilidade']
        impact = inputData['Impacto']

        data = pd.DataFrame({
                "Type of risk": [typeRisk],
                "Impact/Consequences": [impact_Consequence],
                "Project": [project],
                "Metier": [metier],
                "Jalón Affected": [jalon],
                "Probability": [probability],
                "Impact": [impact]
        })


        print("Colunas do new_data:", data.columns)
        print("Colunas esperadas:", preprocessor.transformers_[0][2])

        oneHotEncode = preprocessor.transform(data)

        predictions = model.predict(oneHotEncode)
        predictions_list = predictions.tolist()

        return jsonify({'prediction': predictions_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)