import requests
import os

def get_realtime_oil_prices():
    try:
        # ดึงข้อมูลจาก API บางจากโดยตรง
        url = "https://www.bangchak.co.th/api/oilprice"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # เจาะเข้าไปในชั้นข้อมูลที่เก็บรายการน้ำมัน
            items = data.get('data', {}).get('items', [])
            
            message = "⛽ ราคาน้ำมันวันนี้ (อัปเดตล่าสุด)\n"
            message += "--------------------------\n"
            
            # รายชื่อน้ำมันที่ต้องการแสดงผล
            target_oils = {
                'Hi Premium 97': 'Hi Premium 97',
                'Gasohol 95 E10': 'Gasohol 95 E10',
                'Gasohol E20 S EVO': 'Gasohol E20',
                'Hi Diesel S B7': 'Hi Diesel B7'
            }
            
            found = False
            for item in items:
                oil_name = item.get('OilName', '')
                if oil_name in target_oils:
                    # ดึงราคาปัจจุบัน (Price)
                    price = item.get('Price')
                    message += f"{target_oils[oil_name]}: {price} บาท\n"
                    found = True
            
            if not found:
                return "⛽ ระบบกำลังอัปเดตข้อมูลราคาน้ำมัน"
                
            message += "--------------------------\n"
            message += "รายงานโดย: Bot Phuri"
            return message
        return "❌ ไม่สามารถเชื่อมต่อข้อมูลได้"
    except Exception as e:
        return f"❌ เกิดข้อผิดพลาด: {str(e)}"

def push_message():
    token = os.environ.get('LINE_TOKEN')
    # ID ของคุณภูริ (ตรวจสอบความถูกต้องแล้ว)
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
