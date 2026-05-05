import requests
import os

def get_realtime_oil_prices():
    try:
        url = "https://www.bangchak.co.th/api/oilprice"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            res_json = response.json()
            items = res_json.get('data', {}).get('items', [])
            
            message = "⛽ ราคาน้ำมันวันนี้ (อัปเดตล่าสุด)\n"
            message += "--------------------------\n"
            
            # ใช้การจับคู่แบบ Keyword เพื่อความแม่นยำสูงสุด
            # 'คำค้นหาใน API': 'ชื่อที่จะโชว์ใน LINE'
            oil_config = {
                '97': 'Hi Premium 97',
                '95 S EVO': 'Gasohol 95',
                'E20 S EVO': 'Gasohol E20',
                'ดีเซล S B7': 'Hi Diesel B7'
            }
            
            found_count = 0
            # วนลูปตามลำดับที่เราต้องการโชว์
            for search_key, display_name in oil_config.items():
                for item in items:
                    api_name = item.get('OilName', '')
                    # ถ้าชื่อจาก API มีคำที่เราค้นหาอยู่
                    if search_key in api_name:
                        price = item.get('Pricetoday')
                        if price:
                            message += f"{display_name}: {price} บาท\n"
                            found_count += 1
                            break # เจอตัวนี้แล้ว ไปหาตัวถัดไปใน oil_config
            
            if found_count == 0:
                return "⛽ ระบบกำลังรอการอัปเดตข้อมูลจากสถานี"
                
            message += "--------------------------\n"
            message += "รายงานโดย: Bot Phuri"
            return message
        return "❌ ไม่สามารถติดต่อ API ได้"
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
