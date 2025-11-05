import re
from typing import Dict
from datetime import datetime

def parse_receipt_text(text: str) -> Dict:
    store = None
    date = None
    total = None
    items = None

    date_rgx = re.search(r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b", text)
    total_rgx = re.search(r"(?:Total|TOTAL|Grand\s*Total)[^\d]*(\d[\d.,]*)", text)
    store_rgx = re.search(r"^(.*?)\n", text)  #first line as store name
    item_pattern = r"\d+\s+([A-Za-z\s]+)\s+[\d,.]+"
    items = re.findall(item_pattern, text)

    if store_rgx:
        store = store_rgx.group(1).strip()
        print(store)
    if date_rgx:
        raw_date = date_rgx.group(1)
        for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%Y-%m-%d", "%d/%m/%y", "%d-%m-%y"):
            try:
                parsed_date = datetime.strptime(raw_date, fmt)
                break
            except:
                continue

        date = parsed_date.strftime("%Y/%m/%d")
    if total_rgx:
        total_str = total_rgx.group(1)
        total_str = total_str.replace('.', '').replace(',', '')  # clean total from seperator
        total = int(total_str)
        print(total)

    return {
        "store": store,
        "date": date,
        "total": total,
        "item": items
    }
