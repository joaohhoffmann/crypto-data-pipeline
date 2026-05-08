import boto3
import json
from datetime import datetime


def salva_na_bronze(data, bucket_name):
    s3 = boto3.client("s3")

    date = datetime.now().strftime("%Y-%m-%d")

    file_path = f"bronze/{date}/crypto_raw.json"

    s3.put_object(
        Bucket = bucket_name,
        Key = file_path,
        Body = json.dumps(data, indent=2)
    )

    print(f"Dados salvos na s3://{bucket_name}/{file_path}")





if __name__ == "__main__":
    from src.extract.extract import extrair_dados_crypto

    data = extrair_dados_crypto()
    salva_na_bronze(data, "crypto-pipeline-joao")