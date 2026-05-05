import requests
import os
import json

def get_realtime_oil_prices():
    try:
        # ดึงข้อมูลจาก API บางจาก (Bangchak)
        url = "https://www.bangchak.co.th/api/oilprice"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # ค้นหาราคาน้ำมันจากรายการที่ได้
            items = data.get('data', {}).get('items', [])
            
            message = "⛽ ราคาน้ำมันวันนี้ (อัปเดตล่าสุด)\n"
            message += "--------------------------\n"
            
            # ดึงเฉพาะตัวหลักๆ ที่มึงใช้
            target_oils = {
                'Hi Premium 97': 'Hi Premium 97',
                'Gasohol 95 E10': 'Gasohol 95 E10',
                'Gasohol E20': 'Gasohol E20',
                'Hi Diesel S B7': 'Hi Diesel S B7'
            }
            
            found_any = False
            for item in items:
                oil_name = item.get('OilName')
                if oil_name in target_oils:
                    price = item.get('Price')
                    message += f"{oil_name}: {price} บ.\n"
                    found_any = True
            
            if not found_any:
                return "❌ ไม่พบข้อมูลราคาน้ำมันที่ระบุ"
                
            message += "--------------------------\n"
            message += "ข้อมูลจาก: Bangchak API\n"
            message += "รายงานโดย: Bot Phuri"
            return message
        else:
            return "❌ ดึงข้อมูลจาก API ไม่สำเร็จ (Status Code ไม่ใช่ 200)"
            
    except Exception as e:
        return f"❌ เกิดข้อผิดพลาดในการดึงข้อมูล: {str(e)}"

def push_message():
    token = os.environ.get('LINE_TOKEN')
    # ใช้ ID ของมึงที่เช็คแล้วว่าครบ 33 ตัว
    user_id = 'U9ad765ea3b3a633334cea08ed77d0869

' 

    if not token:
        print("Error: LINE_TOKEN not found.")
        return

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    # เรียกใช้ฟังก์ชันดึงราคาน้ำมันจริง
    message_text = get_realtime_oil_prices()
    
    payload = {
        "to": user_id,
        "messages": [{"type": "text", "text": message_text}]
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        print(f"Response: {res.text}")
        print(f"Status Code: {res.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    push_message()
