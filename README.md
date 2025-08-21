# Real-Time ETL Pipeline from PostgreSQL to Amazon S3

# Overview

This project demonstrates a **real-time ETL pipeline** that captures data from a **PostgreSQL database**, applies lightweight transformations using **Python (Pandas)**, and stores the processed data into **Amazon S3** in **Parquet format**.

The pipeline simulates a retail use case where transactional data must be made available in **near real-time** for downstream **reporting, analytics, and machine learning models**.

By automating ingestion, transformation, and loading, this solution eliminates delays from manual batch uploads and ensures **data freshness** in the data lake.



## Problem Statement

* A retail company captures **transactional data** in PostgreSQL in real time.
* Analytics teams require the data in **Amazon S3** (data lake) with minimal latency.
* Manual batch uploads introduced delays, impacting reporting and decision-making.
* Business required an **automated, near real-time sync** of PostgreSQL → S3.


## Target 

* "Capture new inserts/updates" from PostgreSQL in real-time.
* Apply "light transformations" (date standardization, currency conversion, null handling).
* "Load structured data" into S3, partitioned by date (`/raw/YYYY/MM/DD/`) in "Parquet format".
* Support "automation" via Airflow DAG (optional) or cron jobs.


##  Architecture

```
          +-------------------+
          |   PostgreSQL DB   |
          +---------+---------+
                    |
              Extract (SQL)
                    |
          +---------v---------+
          |  Python ETL Script|
          |  - psycopg2       |
          |  - Pandas         |
          |  - boto3          |
          +---------+---------+
                    |
          Transform & Convert (Parquet)
                    |
          +---------v---------+
          |   Amazon S3       |
          |   /raw/YYYY/MM/DD/|
          +-------------------+
```


# Tech Stack

| Component       | Tool/Service         |
| --------------- | -------------------- |
| Source Database | PostgreSQL           |
| Transformation  | Python (Pandas)      |
| Data Lake       | Amazon S3            |
| Format          | Parquet              |
| Ingestion       | psycopg2 + boto3     |
| Orchestration   | Airflow / cron       |
| Environment     | Local / EC2 / Docker |



##  Setup Instructions

### 1. Prerequisites

* Python 3.8+
* PostgreSQL installed (local or RDS)
* AWS account with S3 bucket
* AWS CLI configured (`aws configure`)
* Install dependencies:

  ```bash
  pip install psycopg2-binary pandas boto3 pyarrow sqlalchemy python-dotenv
  ```



### 2. PostgreSQL Setup

Run the sample SQL script to create and populate tables:

```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    customer_id INT,
    amount NUMERIC(10,2),
    currency VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO transactions (customer_id, amount, currency) VALUES
(1, 100.50, 'USD'),
(2, 250.75, 'USD'),
(3, 75.20, 'EUR');
```

### 3. Environment Variables (`.env`)

Create a `.env` file in your project root:

```ini
PG_HOST=localhost
PG_PORT=5432
PG_DBNAME=retail_db
PG_USER=postgres
PG_PASSWORD=yourpassword

AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
S3_BUCKET=your-bucket-name
S3_PREFIX=retail-data-lake/raw
```

### 4. Run ETL Script

```bash
python etl_postgres_to_s3.py
```

## This will:

* Extract new rows from PostgreSQL.
* Apply transformations (date formatting, currency conversion, null filtering).
* Save as **Parquet**.
* Upload to S3 in **partitioned folders**.



### 5. Optional: Automate with Airflow

* Place `etl_dag.py` in your Airflow DAGs folder.
* Configure scheduling (e.g., every 5 minutes).
* Airflow will automatically execute the ETL pipeline.



## Deliverables

* "SQL script" for PostgreSQL sample data.
* "Python ETL script" (`etl_postgres_to_s3.py`).
* "S3 structured data lake" in Parquet format.
* "Optional Airflow DAG" (`etl_dag.py`).
* "README documentation" (this file).

## Future Improvements

* Implement **Change Data Capture (CDC)** with Debezium or Kafka for high-frequency updates.
* Add **unit tests** for transformations.
* Support **schema evolution** with AWS Glue Catalog.
* Add monitoring & alerting with CloudWatch.



