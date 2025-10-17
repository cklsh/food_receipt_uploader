from fastapi import APIRouter, File, UploadFile
import os, sqlite3
from utils.ocr_reader import text_extract_from_image
from utils.receipt_parser import parse_receipt_text
import re

router = APIRouter()
UPLOAD_DIR = "data/uploads"
DB_PATH = "data/receipts.db"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)


@router.post("/upload")
async def upload_receipt(file: UploadFile = File(...)):
    # saving image into /data
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # extract text using OCR
    text = text_extract_from_image(file_path)

    # parse the receipt info
    parsed = parse_receipt_text(text)

    # DB insertion
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO receipts (filename, store, date, total, raw_text)
        VALUES (?, ?, ?, ?, ?)
    """, (file.filename, parsed["store"], parsed["date"], parsed["total"], ""))

    receipt_id = cur.lastrowid  # id from last insert
    for item in parsed["item"]:
        cur.execute("INSERT INTO receipt_items (receipt_id, item) VALUES (?, ?)", (receipt_id, item))

    conn.commit()
    conn.close()

    return {
        "message": "Success upload the receipt",
        "data": parsed
    }