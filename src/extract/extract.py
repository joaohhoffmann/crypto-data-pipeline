import requests
import json
import boto3
from datetime import datetime

def extrair_dados_crypto():

    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data


def salvar_dados_s3(data, bucket_name):

    s3 = boto3.client("s3")

    date = datetime.now().strftime("%Y-%m-%d")

    file_path = f"bronze/{date}/crypto_raw.json"

    s3.put_object(
        Bucket = bucket_name,
        Key=file_path,
        Body=json.dumps(data, indent=2)
    )

    print(f"Dados salvos na s3://{bucket_name}/{file_path}")


if __name__ == "__main__":
    data = extrair_dados_crypto()
    salvar_dados_s3(data, "crypto-pipeline-joao")
