import requests
import os

def get_realtime_oil_prices():
    try:
        # ดึงข้อมูลราคาน้ำมันจาก API บางจาก
        url = "https://www.bangchak.co.th/api/oilprice"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('data', {}).get('items', [])
            
            message = "⛽ ราคาน้ำมันวันนี้ (อัปเดตล่าสุด)\n"
            message += "--------------------------\n"
            
            found_any = False
            for item in items:
                name = item.get('OilName', '')
                # เช็คชื่อน้ำมันแบบครอบคลุมเพื่อให้ดึงค่ามาแสดงได้แน่นอน
                if any(x in name for x in ['Premium 97', '95 E10', 'E20', 'Diesel S B7']):
                    price = item.get('Price')
                    message += f"{name}: {price} บาท\n"
                    found_any = True
            
            if not found_any:
                return "⛽ ราคาน้ำมันวันนี้\n(กำลังอัปเดตข้อมูลจากระบบ)"
                
            message += "--------------------------\n"
            message += "รายงานโดย: Bot Phuri"
            return message
        return "❌ ไม่สามารถดึงข้อมูลได้ในขณะนี้"
    except Exception as e:
        return f"❌ เกิดข้อผิดพลาด: {str(e)}"

def push_message():
    # ดึง Token จาก GitHub Secrets
    token = os.environ.get('LINE_TOKEN')
    
    # ไอดีผู้ใช้งาน (ตรวจสอบความถูกต้องเรียบร้อยแล้ว)
    user_id = 'U9ad765ea3b3a633334cea08ed77d0869' 

    if not token:
        print("Error: LINE_TOKEN not found.")
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

    res = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {res.status_code}")

if __name__ == "__main__":
    push_message()
