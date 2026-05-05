import requests
import os
import time

def get_oil_price():
    url = "https://api-v2.bangchak.co.th/api/oilprice"
    # ตั้งค่าให้ลองใหม่ได้ 3 ครั้ง ถ้าครั้งแรกพลาด
    for i in range(3):
        try:
            response = requests.get(url, timeout=10) # เพิ่ม timeout กันค้าง
            response.raise_for_status()
            data = response.json()
            items = data['data']['items']
            
            message = "⛽️ ราคาน้ำมันบางจากวันนี้\n"
            message += "------------------\n"
            for item in items:
                # เลือกเฉพาะตัวที่คนใช้บ่อยๆ หรือโชว์ทั้งหมดก็ได้
                message += f"🔹 {item['type']}: {item['price']} บาท\n"
            return message
        except Exception as e:
            if i < 2: # ถ้ายังไม่ครบ 3 ครั้ง ให้รอแป๊บแล้วลองใหม่
                time.sleep(5)
                continue
            return f"เกิดข้อผิดพลาดจากบางจาก: {e}"

def broadcast_to_line(token, text_message):
    line_url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "messages": [{"type": "text", "text": text_message}]
    }
    requests.post(line_url, headers=headers, json=payload)

ACCESS_TOKEN = os.getenv('LINE_TOKEN') 
report = get_oil_price()
if ACCESS_TOKEN:
    broadcast_to_line(ACCESS_TOKEN, report)
