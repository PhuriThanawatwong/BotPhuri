import requests
import os

def get_oil_price():
    # ใช้ API กลางที่รวมราคาน้ำมันทุกยี่ห้อ (รวมบางจากด้วย)
    url = "https://api.chnwt.dev/thai-oil-api/latest"
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
        
        # ดึงข้อมูลของบางจากมาแสดงตามที่คุณ Phuri ชอบ
        bangchak = data['price']['bangchak']
        
        message = "⛽️ ราคาน้ำมันบางจากวันนี้\n"
        message += "------------------\n"
        for type, price in bangchak.items():
            message += f"🔹 {type}: {price} บาท\n"
        return message
    except Exception:
        return "❌ ระบบดึงข้อมูลขัดข้องชั่วคราว ลองใหม่อีกครั้งนะครับ"

def broadcast_to_line(token, text_message):
    line_url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {"messages": [{"type": "text", "text": text_message}]}
    requests.post(line_url, headers=headers, json=payload)

ACCESS_TOKEN = os.getenv('LINE_TOKEN')
report = get_oil_price()
if ACCESS_TOKEN:
    broadcast_to_line(ACCESS_TOKEN, report)
