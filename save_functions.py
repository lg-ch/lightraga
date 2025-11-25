#!/usr/bin/env python3
import boto3

def initialize_client_s3(s3_host: str, akeyid: str, asecretkey: str, AWS_REGION: str):
    return boto3.client(
        "s3",
        endpoint_url=s3_host,
        aws_access_key_id=akeyid,
        aws_secret_access_key=asecretkey,
        region_name=AWS_REGION
    )

def upload_pdf_to_s3(pdf_bytes: bytes, pdf_filename: str,
                     S3_BUCKET: str, S3_PREFIX: str,
                     AWS_REGION: str, s3_host: str,
                     akeyid: str, asecretkey: str) -> str:

    s3 = initialize_client_s3(s3_host, akeyid, asecretkey, AWS_REGION)
    s3_key = f"{S3_PREFIX}{pdf_filename}"

    try:
        s3.head_bucket(Bucket=S3_BUCKET)
    except:
        s3.create_bucket(Bucket=S3_BUCKET)

    s3.put_object(
        Bucket=S3_BUCKET,
        Key=s3_key,
        Body=pdf_bytes,
        ContentType="application/pdf"
    )

    return f"s3://{S3_BUCKET}/{s3_key}"
