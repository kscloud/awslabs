import pymysql
import sys
import os
import boto3
import json

db_address = os.getenv("DB_ADDRESS")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")


def handler(event, context):
    try:
        conn = pymysql.connect(db_address, user=db_username,
                               passwd=db_password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        print(
            "ERROR: Unexpected error: Could not connect to MySQL instance.")
        print(e)
        sys.exit()

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    body = f"s3://{bucket_name}/{object_key}"
    added = event['Records'][0]['eventTime']
    size = event['Records'][0]['s3']['object']['size']

    print(
        f"bucket={bucket_name}, object_key={object_key}, body={body}, added={added}, size={size}")

    try:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS S3Posts (id int NOT NULL AUTO_INCREMENT, body VARCHAR(255) NOT NULL, size INT NOT NULL, added DATETIME, PRIMARY KEY (id))")
            cur.execute(
                f"INSERT INTO S3Posts (body, size, added) VALUES ('{body}', '{size}', '{added}')"
            )
        conn.commit()
    finally:
        conn.close()

    return True
