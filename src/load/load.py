import boto3
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")


def salva_na_bronze(data):
    
    s3 = boto3.client("s3")

    date = datetime.now().strftime("%Y-%m-%d")

    file_path = f"bronze/{date}/crypto_raw.json"

    s3.put_object(
        Bucket = BUCKET_NAME,
        Key = file_path,
        Body = json.dumps(data, indent=2)
    )

    print(f"Dados salvos na s3://{BUCKET_NAME}/{file_path}")


def salva_na_prata(df):
    s3 = boto3.client("s3")

    date = datetime.now().strftime("%Y-%m-%d")

    file_path = f"prata/{date}/crypto_transformed.parquet"

    parquet_data = df.to_parquet(index=False)

    s3.put_object(
        Bucket = BUCKET_NAME,
        Key = file_path,
        Body = parquet_data
    )

