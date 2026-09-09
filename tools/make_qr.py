#!/usr/bin/env python3
"""
Generate the QR codes for the book:

  * qr-code.png        -> the bonus pack home page (back-matter + title page)
  * qr-review.png      -> the review redirect page (/review), which bounces
                          the reader to the book's Amazon review form. The
                          Amazon ASIN is NOT baked into this QR code -- it
                          lives in review.html and can be changed any time
                          without reprinting anything.

Before the real launch:
  1. Set SITE_URL below to the deployed domain.
  2. Re-run this script to regenerate both PNGs.
  3. Rebuild the print PDF so the printed codes are current, and test each
     one at 1 inch minimum before sending to print.

Requires: pip install "qrcode[pil]"
"""
import os
import qrcode

# ---- set this before the real launch ----
SITE_URL   = "https://alaska1.vercel.app/"
REVIEW_URL = SITE_URL.rstrip("/") + "/review"

HERE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(os.path.dirname(HERE), "assets", "img")
os.makedirs(IMG_DIR, exist_ok=True)

TARGETS = {
    "qr-code.png":   SITE_URL,
    "qr-review.png": REVIEW_URL,
}

for filename, url in TARGETS.items():
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # tolerant of print wear
        box_size=20,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0a1b29", back_color="#f5f1e6")
    out = os.path.join(IMG_DIR, filename)
    img.save(out)
    print(f"wrote {out}  ({img.size[0]}x{img.size[1]}px)  ->  {url}")

if "YOUR-" in SITE_URL or "example" in SITE_URL:
    print("WARNING: SITE_URL still looks like a placeholder")
