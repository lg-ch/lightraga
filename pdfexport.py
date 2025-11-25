#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import save_functions

def export_pdf(url: str, pdf_filename: str,
               S3_BUCKET: str, S3_PREFIX: str,
               AWS_REGION: str, s3_host: str,
               akeyid: str, asecretkey: str):

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        # attendre les tableaux dynamiques
        try:
            page.wait_for_selector("div.euiDataGridRow", timeout=20000)
        except:
            pass

        # forcer le lazy loading des images
        page.evaluate("""
            document.querySelectorAll('img[loading="lazy"]').forEach(img => {
                img.loading = "eager";
                img.src = img.src;
            });
        """)
        try:
            page.wait_for_function("() => Array.from(document.images).every(i => i.complete)", timeout=20000)
        except:
            pass

        pdf_bytes = page.pdf(format="A4", print_background=True)
        browser.close()

        s3_path = save_functions.upload_pdf_to_s3(
            pdf_bytes, pdf_filename, S3_BUCKET, S3_PREFIX,
            AWS_REGION, s3_host, akeyid, asecretkey
        )

        print(f"[✔] Fichier envoyé sur : {s3_path}")
        return s3_path



