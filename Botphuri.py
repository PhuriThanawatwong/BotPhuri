import requests
import os

def get_oil_price():
    # ใช้ API กลางที่รวมราคาน้ำมันทุกยี่ห้อ
    url = "http://www.eppo.go.th/index.php/th/petroleum/price/oil-price"
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
        
        # เปลี่ยนจาก 'bangchak' เป็น 'ptt' เพื่อดึงข้อมูลของ ปตท.
        ptt = data['price']['ptt']
        
        message = "⛽️ ราคาน้ำมัน วันนี้\n"
        message += "------------------\n"
        for type, price in ptt.items():
            # กรองเฉพาะประเภทที่มีราคา (บางรายการอาจเป็น null หรือไม่มีข้อมูล)
            if price:
                message += f"⛽️ {type}: {price} บาท\n"
        return message
    except Exception as e:
        return f"❌ ระบบดึงข้อมูลขัดข้องชั่วคราว: {str(e)}"

def broadcast_to_line(token, text_message):
    line_url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Content-Type": "application/json", 
        "Authorization": f"Bearer {token}"
    }
    payload = {"messages": [{"type": "text", "text": text_message}]}
    requests.post(line_url, headers=headers, json=payload)

# ส่วนการรันโปรแกรม
ACCESS_TOKEN = os.getenv('LINE_TOKEN')
report = get_oil_price()

if ACCESS_TOKEN:
    broadcast_to_line(ACCESS_TOKEN, report)
    print("ส่งข้อมูลราคาน้ำมัน ปตท. เรียบร้อยแล้ว!")
else:
    print("ไม่พบ LINE_TOKEN ใน Environment Variable")
    print(report) # แสดงผลใน Terminal แทนถ้าไม่มี Token
