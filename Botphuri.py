import requests
import os
import json

def get_realtime_oil_prices():
    try:
        url = "https://www.bangchak.co.th/api/oilprice"
        response = requests.get(url, timeout=15)
        
        # ป้องกัน 'str' has no attribute 'get' โดยการเช็คประเภทข้อมูลก่อน
        try:
            res_data = response.json()
        except:
            return "⛽ ระบบ API บางจากขัดข้องชั่วคราว"

        # เจาะเข้าโครงสร้าง data -> items (กูเช็คมาแล้ว รอบนี้มาแน่)
        items = res_data.get('data', {}).get('items', [])
        
        message = "⛽ ราคาน้ำมันวันนี้ (อัปเดตล่าสุด)\n"
        message += "--------------------------\n"
        
        # ชื่อน้ำมันแบบเป๊ะๆ จากฐานข้อมูลบางจาก
        targets = {
            'ไฮพรีเมียม 97 แก๊สโซฮอล์ 95++': 'Hi Premium 97',
            'แก๊สโซฮอล์ 95 S EVO': 'Gasohol 95',
            'แก๊สโซฮอล์ E20 S EVO': 'Gasohol E20',
            'ไฮดีเซล S B7': 'Hi Diesel B7'
        }
        
        found_count = 0
        for item in items:
            name = item.get('OilName', '')
            if name in targets:
                # ใช้ Pricetoday เท่านั้น
                price = item.get('Pricetoday')
                if price:
                    message += f"{targets[name]}: {price} บาท\n"
                    found_count += 1
        
        if found_count == 0:
            return "⛽ กำลังรอข้อมูลราคาจากหน้าสถานี"
            
        message += "--------------------------\n"
        message += "รายงานโดย: Bot Phuri"
        return message
    except Exception as e:
        return f"❌ ข้อผิดพลาด: {str(e)}"

def push_message():
    token = os.environ.get('LINE_TOKEN')
    user_id = 'U9ad765ea3b3a633334cea08ed77d0869' # ไอดีมึง

    if not token: return

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    oil_text = get_realtime_oil_prices()
    
    payload = {
        "to": user_id,
        "messages": [{"type": "text", "text": oil_text}]
    }

    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    push_message()
