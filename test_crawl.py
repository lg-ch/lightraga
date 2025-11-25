from crawler import crawl

RSS_URL = "https://thedfirreport.com/feed/"
STATE_FILE = "last_test.txt"

S3_BUCKET = "dfir-reports"
S3_PREFIX = "tests/"
AWS_REGION = "us-east-1"

# MinIO local
s3_host = "http://172.23.0.2:9000"
akeyid = "minioadmin"
asecretkey = "minioadmin"

crawl(RSS_URL, STATE_FILE, S3_BUCKET, S3_PREFIX,
      AWS_REGION, s3_host, akeyid, asecretkey)
