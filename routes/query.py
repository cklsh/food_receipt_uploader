from fastapi import APIRouter, Query
import sqlite3
import re
from datetime import datetime, timedelta

router = APIRouter()

DB_PATH = "data/receipts.db"

@router.get("/query")
def query_receipts(question: str = Query(...)):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    q = question.lower()
    today = datetime.now().date()
    
    # ex: What food did I buy yesterday?
    if "yesterday" in q and ("buy" in q or "food" in q):
        date_target = today - timedelta(days=1)

        cur.execute("""
            SELECT item, price FROM receipt_items
            JOIN receipts ON receipts.id = receipt_items.receipt_id
            WHERE receipts.date = ?
        """, (date_target.strftime("%Y/%m/%d"),))
        data = cur.fetchall()

        result = [{"item": i, "price": p} for i, p in data]
        return {"question": question, "result": result}
    
    # ex: Total expenses on a date
    date_query = re.search(r"(\d{4})[/-](\d{1,2})[/-](\d{1,2})", q)
    if "total" in q or "expense" in q:
        if date_query:
            year, month, day = date_query.groups()
            date_in_str = f"{year}/{int(month):02}/{int(day):02}"
            cur.execute("""
                SELECT SUM(total) FROM receipts
                WHERE date = ?
            """, (date_in_str,))
            total = cur.fetchone()[0] or 0.0

            return {"question": q, "total_expense": total}

    # ex: Where did I buy [item] from last [n] day
    item_query = re.search(r"(?:buy|eat)\s+([a-zA-Z\s]+?)(?:\s+from|\s+on|$)", q, re.IGNORECASE)
    if "where" in q and item_query:
        item = item_query.group(1).strip()
        start_date = today - timedelta(days=100)
        start_date_str = start_date.strftime("%Y/%m/%d")
        cur.execute("""
            SELECT DISTINCT store FROM receipts
            JOIN receipt_items ON receipts.id = receipt_items.receipt_id
            WHERE receipts.date >= ? AND LOWER(item) LIKE LOWER(?)
        """, (start_date_str, f"%{item}%"))

        stores = [row[0] for row in cur.fetchall()]
        return {"question": question, "stores": stores}

    conn.close()
    return {"message": "Please try another question"}
