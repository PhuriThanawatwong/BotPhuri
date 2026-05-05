import requests
import os
import time

def get_oil_price():
    # รายชื่อแหล่งข้อมูล (เรียงลำดับความสำคัญ)
    sources = [
        {"name": "บางจาก", "url": "https://api-v2.bangchak.co.th/api/oilprice", "type": "json_bc"},
        {"name": "ปตท. (OR)", "url": "https://api.iservices.me/api/oil/latest", "type": "json_generic"}
    ]

    for source in sources:
        try:
            print(f"กำลังดึงข้อมูลจาก: {source['name']}")
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
            
            return message # ถ้าสำเร็จให้ส่งข้อความออกไปเลย
        except Exception as e:
            print(f"แหล่งข้อมูล {source['name']} มีปัญหา: {e}")
            continue # ถ้าพลาด ให้ไปลองแหล่งข้อมูลถัดไป
            
    return "❌ ไม่สามารถดึงข้อมูลราคาน้ำมันได้จากทุกแหล่งในขณะนี้"

def broadcast_to_line(token, text_message):
    line_url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {"messages": [{"type": "text", "text": text_message}]}
    requests.post(line_url, headers=headers, json=payload)

ACCESS_TOKEN = os.getenv('LINE_TOKEN') 
report = get_oil_price()
if ACCESS_TOKEN:
    broadcast_to_line(ACCESS_TOKEN, report)​
