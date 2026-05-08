import boto3
import json
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = os.getenv('BUCKET_NAME')



def ler_dados_bronze():
    s3 = boto3.client('s3')

    date = datetime.now().strftime('%Y-%m-%d')
    file_path = f"bronze/{date}/dados.json"

    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=file_path
    )

    data = json.load(response['Body'].read().decode('utf-8'))

    return data


def transformar_dados(data):
    df = pd.DataFrame(data)

    colunas_remover = [
        'image',
        'roi',
        'fully_diluted_valuation'
    ]

    df = df.drop(columns=colunas_remover, errors='ignore')

    df['last_updated'] = pd.to_datetime(df['last_updated'])
    df['ath_date'] = pd.to_datetime(df['ath_date'])
    
    df["max_supply"] = pd.to_numeric(df['max_supply'].fillna(0))

    df["data_extracao"] = datetime.now().strftime('%Y-%m-%d')

    return df
