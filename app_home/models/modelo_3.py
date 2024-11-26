import os
from joblib import dump
import joblib
import pandas as pd
from sklearn.metrics import precision_score
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from warnings import simplefilter




def Machine_Learning():
# Ignorando warnings
    simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

    # Carregando o arquivo
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

        #Type of risk, Impact/Consequences, Project, Metier, Jalón Affecte, Probability, Impact

        df.fillna('Desconhecido', inplace=True)
        le = LabelEncoder()

        print("Nomes das colunas:")
        print(df.columns)

        Y = df['Risk rating']
        X = df.drop('Risk rating', axis=1)

        categorical_columns = X.select_dtypes(include=['object']).columns

        preprocessor = ColumnTransformer(
            transformers=[('Renault', OneHotEncoder(handle_unknown='ignore'), categorical_columns)],
            remainder='passthrough'
        )

        X_transformed = preprocessor.fit_transform(X)

        X_train, X_test, Y_train, Y_test = train_test_split(X_transformed, Y, test_size=0.30, random_state=42)

        model = RandomForestClassifier(n_estimators=200, criterion="entropy", max_depth=10, n_jobs=2)
        model.fit(X_train, Y_train)

        dump(preprocessor, 'preprocessor.joblib')
        dump(model, 'model.joblib')

        train_predictions = model.predict(X_train)
        test_predictions = model.predict(X_test)

        print(f"Precisão no conjunto de treinamento: {precision_score(Y_train, train_predictions, average='weighted'):.2f}")
        print(f"Precisão no conjunto de teste: {precision_score(Y_test, test_predictions, average='weighted'):.2f}")

        Ypred = model.predict(X_transformed)
        plt.plot(Y.reset_index(drop=True), label='True Labels')
        plt.plot(Ypred, label='Predicted Labels')
        plt.legend()
        plt.show()

    except FileNotFoundError:
        print(f"O arquivo {file_path} não foi encontrado. Verifique o caminho e tente novamente.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")