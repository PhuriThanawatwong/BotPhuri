import requests
import os

def get_oil_price():
    try:
        # ใช้ API ของ OR (PTT) ซึ่งเป็นแหล่งข้อมูลที่นิ่งที่สุดในไทย
        url = "https://orapiweb.pttor.com/api/oilprice/LatestPrices"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'th-TH,th;q=0.9'
        }
        response = requests.get(url, headers=headers, timeout=20)
        oil_list = response.json()
        
        message = "⛽ ราคาน้ำมันล่าสุด (PTT)\n"
        message += "--------------------------\n"
        
        # รายชื่อน้ำมันที่มึงต้องใช้ในชีวิตประจำวัน
        targets = ["Gasohol 95", "Gasohol E20", "Super Power Gasohol 95", "Diesel B7"]
        found = False
        
        for item in oil_list:
            name = item.get('productName')
            price = item.get('price')
            
            if name in targets:
                if price and str(price) not in ["0", "None", ""]:
                    message += f"{name}: {price} บาท\n"
                    found = True
        
        if not found:
            return "⛽ ขออภัย: ระบบต้นทางยังไม่อัปเดตตัวเลข"
            
        message += "--------------------------\n"
        message += "รายงานโดย: Bot Phuri"
        return message
    except Exception as e:
        return f"❌ ระบบขัดข้อง: {str(e)}"

def push_message():
    # ดึงค่าจาก GitHub Secrets
    token = os.environ.get('LINE_TOKEN')
    user_id = os.environ.get('USER_ID') or 'U9ad765ea3b3a633334cea08ed77d0869'
    
    if not token:
        return

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    oil_text = get_oil_price()
    payload = {
        "to": user_id,
        "messages": [{"type": "text", "text": oil_text}]
    }

    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    push_message()
