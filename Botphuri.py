import requests
import os

def get_realtime_oil_prices():
    try:
        # ดึงข้อมูลจาก API บางจาก
        url = "https://www.bangchak.co.th/api/oilprice"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('data', {}).get('items', [])
            
            message = "⛽ ราคาน้ำมันวันนี้ (อัปเดตล่าสุด)\n"
            message += "--------------------------\n"
            
            # ตั้งค่าคำสำคัญเพื่อค้นหาน้ำมันที่ต้องการ
            targets = {
                'Premium 97': 'Hi Premium 97',
                '95 E10': 'Gasohol 95',
                'E20': 'Gasohol E20',
                'Diesel S B7': 'Hi Diesel B7'
            }
            
            found_data = []
            for item in items:
                oil_name = item.get('OilName', '')
                for key, display_name in targets.items():
                    if key in oil_name:
                        price = item.get('Price')
                        found_data.append(f"{display_name}: {price} บาท")
            
            if found_data:
                # เรียงข้อมูลและรวมเข้าด้วยกัน
                message += "\n".join(found_data)
            else:
                message += "ขออภัย ระบบกำลังปรับปรุงฐานข้อมูล"
                
            message += "\n--------------------------\n"
            message += "รายงานโดย: Bot Phuri"
            return message
        return "❌ ไม่สามารถเชื่อมต่อข้อมูลได้"
    except Exception as e:
        return f"❌ เกิดข้อผิดพลาด: {str(e)}"

def push_message():
    token = os.environ.get('LINE_TOKEN')
    user_id = 'U9ad765ea3b3a633334cea08ed77d0869' 

    if not token:
        return

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
