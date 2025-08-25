import os
import psycopg2
import pandas as pd
import boto3
import pyarrow as pa
import pyarrow.parquet as pq
from io import BytesIO
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL config
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DBNAME = os.getenv("PG_DBNAME")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

# AWS config
S3_BUCKET = os.getenv("S3_BUCKET")
S3_PREFIX = os.getenv("S3_PREFIX")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")

# Extraction config
last_extraction_time = os.getenv("LAST_EXTRACTION_TIME")
if not last_extraction_time:
    raise ValueError("LAST_EXTRACTION_TIME not set in environment variables")

def extract_data():
    try:
        conn = psycopg2.connect(
            host=PG_HOST, port=PG_PORT, dbname=PG_DBNAME,
            user=PG_USER, password=PG_PASSWORD
        )
        query = f"""
            SELECT * FROM employees
            WHERE hire_date > '{last_extraction_time}'
        """
        print(f"Running query:\n{query}")
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error extracting data: {e}")
        return pd.DataFrame()

def transform_data(df):
    if 'hire_date' in df.columns:
        df['hire_date'] = pd.to_datetime(df['hire_date']).dt.strftime('%Y-%m-%d')
    if 'department' in df.columns:
        df['department'] = df['department'].str.upper()
    return df

def load_to_s3(df):
    try:
        table = pa.Table.from_pandas(df)
        buffer = BytesIO()
        pq.write_table(table, buffer)
        buffer.seek(0)

        today = datetime.utcnow()
        date_folder = today.strftime("%Y-%m-%d")
        s3_path = f"{S3_PREFIX}/{date_folder}/employees.parquet"

        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION
        )
        s3.upload_fileobj(buffer, S3_BUCKET, s3_path)
        print(f"Uploaded to s3://{S3_BUCKET}/{s3_path}")
    except Exception as e:
        print(f"Error uploading to S3: {e}")

if __name__ == "__main__":
    print(f"LAST_EXTRACTION_TIME is set to: {last_extraction_time}")
    df = extract_data()
    if not df.empty:
        df = transform_data(df)
        load_to_s3(df)
    else:
        print("No new data to process.")
