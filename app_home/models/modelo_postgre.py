from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import precision_score
from joblib import dump
import pandas as pd
import psycopg
import os
import matplotlib.pyplot as plt
from warnings import simplefilter
from dotenv import load_dotenv
import joblib

# Carregar variáveis do arquivo .env
load_dotenv()

# Verifique se todas as variáveis estão sendo carregadas corretamente
# print(f"Conectando ao banco: {database} no host {host} na porta {port}")
# print(f"Usuário: {usuario}")
# print(f"Senha: {senha}")

def Machine_Learning():
    # Ignorando warnings
    simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

    load_dotenv()

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")
    usuario = os.getenv("DB_USER")
    senha = os.getenv("DB_PASSWORD")

    print(f"Conectando ao banco: {database} no host {host} na porta {port}")
    print(f"Usuário: {usuario}")
    print(f"Senha: {senha}")

    # Carregando o arquivo
    try:
        with psycopg.connect(
            host=host,
            port=port,
            dbname=database,
            user=usuario,
            password=senha
        ) as conn:
            
            print("Conexão bem-sucedida!")
            query = "SELECT * FROM tb_risks;"

            # Limpeza e processamento de dados
            df = pd.read_sql(query, conn)

            
        df.columns = df.columns.str.strip()

        df.drop(
            [
                'rsk_id', 'rsk_description', 'rsk_responsible_area', 'rsk_consequence',
                'rsk_alert_date', 'rsk_created_at', 'rsk_updated_at', 'rsk_usr_id'
            ],
            axis=1,
            inplace=True
        )
        #rsk_type, rsk_probability, rsk_project_id, rsk_impact, rsk_plant, rsk_jalon, rsk_metier, rsk_status 

        df.fillna(0, inplace=True)


        Y = df['rsk_classification']
        X = df.drop('rsk_classification', axis=1)

        print("Nomes das colunas:")
        print(X.columns)
        # categorical_columns = X.select_dtypes(include=['object']).columns

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.30, random_state=42)

        model = RandomForestClassifier(n_estimators=100, criterion="entropy", max_depth=5, n_jobs=2)
        model.fit(X_train, Y_train)

        dump(model, 'models/model.joblib')

        train_predictions = model.predict(X_train)
        test_predictions = model.predict(X_test)

        print(f"Precisão no conjunto de treinamento: {precision_score(Y_train, train_predictions, average='weighted'):.2f}")
        print(f"Precisão no conjunto de teste: {precision_score(Y_test, test_predictions, average='weighted'):.2f}")

        Ypred = model.predict(X)
        plt.plot(Y.reset_index(drop=True), label='True Labels')
        plt.plot(Ypred, label='Predicted Labels')
        plt.legend()
        plt.show()

    except Exception as e:
        print("Erro ao conectar ou executar a query:", e)
