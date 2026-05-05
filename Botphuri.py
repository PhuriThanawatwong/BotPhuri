import requests
import os

def get_realtime_oil_prices():
    try:
        # ดึงข้อมูลจาก API บางจากโดยตรง
        url = "https://www.bangchak.co.th/api/oilprice"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            res_json = response.json()
            # โครงสร้างจริงอยู่ใน data -> items
            items = res_json.get('data', {}).get('items', [])
            
            message = "⛽ ราคาน้ำมันวันนี้ (อัปเดตล่าสุด)\n"
            message += "--------------------------\n"
            
            # ตั้งค่าชื่อที่จะแสดงคู่กับ Keyword ที่จะหาในชื่อน้ำมัน
            oil_config = {
                'Premium 97': 'Hi Premium 97',
                '95 S EVO': 'Gasohol 95',
                'E20 S EVO': 'Gasohol E20',
                'ไฮดีเซล S B7': 'Hi Diesel B7'
            }
            
            found_count = 0
            for display_name, keyword in [(v, k) for k, v in oil_config.items()]:
                for item in items:
                    api_name = item.get('OilName', '')
                    # ถ้าเจอ Keyword ในชื่อที่ API ส่งมา
                    if keyword in api_name:
                        price = item.get('Pricetoday') # ต้องใช้ตัวนี้ถึงจะมีเลขราคา
                        if price:
                            message += f"{display_name}: {price} บาท\n"
                            found_count += 1
                            break
            
            if found_count == 0:
                return "⛽ ระบบกำลังรอการอัปเดตข้อมูลราคาน้ำมัน"
                
            message += "--------------------------\n"
            message += "รายงานโดย: Bot Phuri"
            return message
        return "❌ เชื่อมต่อ API ไม่สำเร็จ"
    except Exception as e:
        return f"❌ เกิดข้อผิดพลาด: {str(e)}"

def push_message():
    token = os.environ.get('LINE_TOKEN')
    user_id = 'U9ad765ea3b3a633334cea08ed77d0869' # ID 33 ตัวของคุณภูริ

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
