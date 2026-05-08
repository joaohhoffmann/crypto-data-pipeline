import boto3
import pandas as pd
import os
from io import BytesIO
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = os.getenv('BUCKET_NAME')

def ler_dados_prata():

    s3 = boto3.client('s3')

    date = datetime.now().strftime('%Y-%m-%d')

    file_path = f"prata/{date}/crypto_transformed.parquet"

    response = s3.get_object(
        Bucket = BUCKET_NAME,
        Key = file_path,
    )

    parquet_data = BytesIO(response['Body'].read())
    df = pd.read_parquet(parquet_data)

    return df

def agregar_metricas(df):
    market_cap_total = df['market_cap'].sum()
    df["dominancia_mercado"] = round((df['market_cap'] / market_cap_total) * 100, 2)

    df["volatilidade_24h"] = round(df["high_24h"] - df["low_24h"], 2)

    df["volume_por_market_cap"] = round((df["total_volume"] / df["market_cap"]) * 100, 2)

    df = df.sort_values("market_cap", ascending=False).reset_index(drop=True)

    df["ranking"] = df.index + 1

    colunas_gold = [
        "ranking",
        "name",
        "symbol",
        "current_price",
        "market_cap",
        "dominancia_mercado",
        "total_volume",
        "volume_por_market_cap",
        "high_24h",
        "low_24h",
        "volatilidade_24h",
        "price_change_percentage_24h",
        "circulating_supply",
        "max_supply",
        "data_extracao"
    ]

    df_gold = df[colunas_gold]
    return df_gold


if __name__ == "__main__":
    from src.load.load import salva_na_ouro

    df = ler_dados_prata()

    df_gold = agregar_metricas(df)

    salva_na_ouro(df_gold)
    print(df_gold.head(10))