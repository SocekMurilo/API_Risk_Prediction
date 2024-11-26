import os
import pandas as pd

from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer


from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, KFold
from scikeras.wrappers import KerasClassifier


file_path = 'DataSet/Renault.xlsm'

if os.path.exists(file_path):
    print(f"O arquivo {file_path} foi encontrado.")
else:
    print(f"O arquivo {file_path} NÃO foi encontrado.")

try:
    # Limpeza e processamento de dados

    df = pd.read_excel(file_path, header=4, usecols="C:AF", sheet_name="List of risks")

    df.columns = df.columns.str.strip()

    df.drop(
        [
            'Risk', 'Area Responsible for identification', 'Risk Entry Date', 
            'Impacted Jalón in the future', 'Impact Renault', 
            'Strategy', 'Action','Pilot Name', 'Pilot ID', 'Initial Plan Date',
            'Alert Date','Resolution Time', 'Time', 'Comments', 'Residual Probability',
            'Residual Impact', 'Residual Risk Rating', 'Action validation',
            'Risk validation', 'Resolution date', 'Status', 'Capitalization'
        ],
        axis=1,
        inplace=True
    )

    df.fillna('Desconhecido', inplace=True)
    le = LabelEncoder()

    print(f"Nomes das colunas: {df.select_dtypes(include=['object']).columns}")

    Y = df['Risk rating']
    X = df.drop('Risk rating', axis=1)

    columns_labelEncoder = ['Probability', 'Impact']
    columns_oneHotEncoder = ['Type of risk', 'Impact/Consequences', 'Project', 'Metier', 'Jalón Affected']
    
    categorical_columns = X.select_dtypes(include=['object']).columns

    for columns in columns_labelEncoder:
        X[f'{columns}'] = le.fit_transform(X[f'{columns}'])

    preprocessor = ColumnTransformer(
        transformers=[
            ('Renault', OneHotEncoder(handle_unknown='ignore'), columns_oneHotEncoder)
        ],
        remainder='passthrough'
    )

    # Modelo da IA 
    model = RandomForestClassifier()

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])

    kf = KFold(n_splits=10, shuffle=True, random_state=42)
    scores = cross_val_score(pipeline, X, Y, cv=kf)

    print(f"Scores de validação cruzada: {scores}")
    print(f"Acurácia média: {scores.mean()}")

except FileNotFoundError:
    print(f"O arquivo {file_path} não foi encontrado. Verifique o caminho e tente novamente.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
