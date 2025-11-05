# Food Receipt Uploader

A Python application that reads and stores food purchase receipts using OCR (Optical Character Recognition).  
It extracts text from receipt images, saves the data to an SQLite database, and supports basic natural-language queries such as:
- “What food did I buy yesterday?”
- “Total expenses on 2025/10/31”

---

## Features

- OCR text extraction using `utils.ocr_reader.text_extract_from_image`
- SQLite database for storing receipts and items
- Simple rule-based question answering logic
- Dockerized for easy deployment
- CI/CD with GitHub Actions (linting and build checks)

---

## How It Works

The app uses OCR to extract text from receipt images, then stores the results in a database.  
Users can run simple question-like queries, which are parsed into SQL commands.

Example logic:

```python
# Example: "What food did I buy yesterday?"
if "yesterday" in q and ("buy" in q or "food" in q):
    date_target = today - timedelta(days=1)
    cur.execute("""
        SELECT item, price FROM receipt_items
        JOIN receipts ON receipts.id = receipt_items.receipt_id
        WHERE receipts.date = ?
    """, (date_target.strftime("%Y/%m/%d"),))
    data = cur.fetchall()

# Example: "Total expenses on 2025/10/31"
if "total" in q or "expense" in q:
    if date_query:
        cur.execute("""
            SELECT SUM(total) FROM receipts WHERE date = ?
        """, (date_in_str,))
        total = cur.fetchone()[0] or 0.0

```
Installation
```bash
git clone https://github.com/cklsh/food_receipt_uploader.git
cd food_receipt_uploader
```
Set up environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Run the app
```
Run the app
```bash
python main.py
```

Run with Docker
```bash
docker build -t food-receipt-uploader .
docker run -p 8000:8000 food-receipt-uploader
```
## CI/CD
The GitHub Actions workflow (.github/workflows/ci.yml) runs automatically on each push and pull request to the main branch.

Includes:
Linting with flake8 (ignores line-length errors) and
Docker build check

```yaml
- name: Lint python code
  run: flake8 . --ignore=E501

- name: Build Docker image
  run: docker build -t food-receipt-uploader .
```

Author
cklsh
