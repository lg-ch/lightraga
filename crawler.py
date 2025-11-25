#!/usr/bin/env python3
import feedparser
import os
import time
from datetime import datetime
from pdfexport import export_pdf

def load_last_processed(STATE_FILE):
    if os.path.exists(STATE_FILE):
        return open(STATE_FILE).read().strip()
    return None

def save_last_processed(report_id, STATE_FILE):
    with open(STATE_FILE, "w") as f:
        f.write(report_id)

def crawl(RSS_URL, STATE_FILE,
          S3_BUCKET, S3_PREFIX, AWS_REGION,
          s3_host, akeyid, asecretkey):

    feed = feedparser.parse(RSS_URL)
    last_id = load_last_processed(STATE_FILE)
    new_reports = []

    for entry in feed.entries:
        entry_id = entry.get("id") or entry.get("link")
        if last_id and entry_id == last_id:
            break
        new_reports.append((entry.title, entry.link, entry_id))

    new_reports.reverse()

    for title, url, entry_id in new_reports:

        safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).strip()
        pdf_filename = safe_title + ".pdf"

        print(f"\n[+] Nouveau rapport : {title}\n → {url}")
        try:
            s3_path = export_pdf(
                url, pdf_filename, S3_BUCKET, S3_PREFIX,
                AWS_REGION, s3_host, akeyid, asecretkey
            )
            print(f"[✔] Stocké : {s3_path}")
            save_last_processed(entry_id, STATE_FILE)
        except Exception as e:
            print(f"[!!] Erreur : {e}")

        time.sleep(10)








