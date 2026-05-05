import requests
import os
import time

def get_oil_price():
    sources = [
        {"name": "บางจาก", "url": "https://api-v2.bangchak.co.th/api/oilprice", "type": "json_bc"},
        {"name": "ปตท. (OR)", "url": "https://api.iservices.me/api/oil/latest", "type": "json_generic"}
    ]
    for source in sources:
        try:
            response = requests.get(source['url'], timeout=15)
            response.raise_for_status()
            message = f"⛽️ ราคาน้ำมันวันนี้ ({source['name']})\n"
            message += "------------------\n"
            if source['type'] == "json_bc":
                data = response.json()
                items = data['data']['items']
                for item in items:
                    message += f"🔹 {item['type']}: {item['price']} บาท\n"
            else:
                data = response.json()
                for item in data['data']:
                    message += f"🔹 {item['type']}: {item['price']} บาท\n"
            return message
        except Exception:
            continue
    return "❌ ไม่สามารถดึงข้อมูลได้"

def broadcast_to_line(token, text_message):
    line_url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {"messages": [{"type": "text", "text": text_message}]}
    requests.post(line_url, headers=headers, json=payload)

ACCESS_TOKEN = os.getenv('LINE_TOKEN')
report = get_oil_price()
if ACCESS_TOKEN:
    broadcast_to_line(ACCESS_TOKEN, report)
