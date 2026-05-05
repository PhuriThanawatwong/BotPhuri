import requests
import os

def get_realtime_oil_prices():
    try:
        # ยิงเข้า API บางจาก
        url = "https://www.bangchak.co.th/api/oilprice"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            res_json = response.json()
            # โครงสร้างใหม่: ข้อมูลอยู่ที่ data และวนลูปได้เลย
            items = res_json.get('data', [])
            
            message = "⛽ ราคาน้ำมันวันนี้ (อัปเดตล่าสุด)\n"
            message += "--------------------------\n"
            
            # จับคู่ Keyword ที่มักจะมีในชื่อน้ำมันของบางจาก
            targets = {
                '97': 'Hi Premium 97',
                '95 S EVO': 'Gasohol 95',
                'E20 S EVO': 'Gasohol E20',
                'ดีเซล S B7': 'Hi Diesel B7'
            }
            
            found_count = 0
            for search_key, display_name in targets.items():
                for item in items:
                    api_name = item.get('OilName', '')
                    if search_key in api_name:
                        # ใช้ field 'Pricetoday' เพื่อเอาเลขราคาปัจจุบัน
                        price = item.get('Pricetoday')
                        if price:
                            message += f"{display_name}: {price} บาท\n"
                            found_count += 1
                            break
            
            if found_count == 0:
                return "⛽ ระบบกำลังรอข้อมูลราคาจาก API บางจาก"
                
            message += "--------------------------\n"
            message += "รายงานโดย: Bot Phuri"
            return message
        return "❌ เชื่อมต่อ API บางจากไม่ได้"
    except Exception as e:
        return f"❌ ข้อผิดพลาด: {str(e)}"

def push_message():
    token = os.environ.get('LINE_TOKEN')
    user_id = 'U9ad765ea3b3a633334cea08ed77d0869' # ไอดีมึง

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
