import requests
import os

def get_realtime_oil_prices():
    try:
        # ดึงข้อมูลจาก API บางจากโดยตรง
        url = "https://www.bangchak.co.th/api/oilprice"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            res_json = response.json()
            # โครงสร้าง API อยู่ใน data -> items
            items = res_json.get('data', {}).get('items', [])
            
            message = "⛽ ราคาน้ำมันวันนี้ (อัปเดตล่าสุด)\n"
            message += "--------------------------\n"
            
            # ตั้งค่าชื่อที่จะแสดงผลคู่กับ Keyword ที่ค้นหาใน API
            oil_map = {
                'Premium 97': 'Hi Premium 97',
                '95 S EVO': 'Gasohol 95',
                'E20 S EVO': 'Gasohol E20',
                'ไฮดีเซล S B7': 'Hi Diesel B7'
            }
            
            found_count = 0
            # วนลูปเช็คข้อมูลน้ำมันทีละตัว
            for display_name in oil_map.values():
                for item in items:
                    api_oil_name = item.get('OilName', '')
                    # ตรวจสอบว่าชื่อน้ำมันใน API ตรงกับที่เราต้องการไหม
                    if any(key in api_oil_name for key in oil_map.keys() if oil_map[key] == display_name):
                        # ดึงราคาจากฟิลด์ Pricetoday ตามโครงสร้าง API จริง
                        price = item.get('Pricetoday')
                        if price:
                            message += f"{display_name}: {price} บาท\n"
                            found_count += 1
                            break # เจอแล้วไปหาตัวถัดไป
            
            if found_count == 0:
                return "⛽ ระบบกำลังรอการอัปเดตข้อมูลราคาน้ำมัน"
                
            message += "--------------------------\n"
            message += "รายงานโดย: Bot Phuri"
            return message
        return "❌ ไม่สามารถเชื่อมต่อกับฐานข้อมูลได้"
    except Exception as e:
        return f"❌ เกิดข้อผิดพลาด: {str(e)}"

def push_message():
    token = os.environ.get('LINE_TOKEN')
    # ยืนยันไอดีผู้ใช้ของคุณภูริ (33 ตัวอักษร)
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
