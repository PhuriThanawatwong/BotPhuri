import requests
import os

def get_realtime_oil_prices():
    try:
        url = "https://www.bangchak.co.th/api/oilprice"
        response = requests.get(url, timeout=15)
        res_data = response.json()
        items = res_data.get('data', {}).get('items', [])
        
        message = "⛽ ราคาน้ำมันวันนี้ (อัปเดตล่าสุด)\n"
        message += "--------------------------\n"
        
        # ใช้รหัส ID ของน้ำมันแทนชื่อ (วิธีที่ชัวร์ที่สุด)
        # 1=95 S EVO, 2=E20 S EVO, 14=Hi Premium 97, 8=Hi Diesel B7
        target_ids = {
            '14': 'Hi Premium 97',
            '1': 'Gasohol 95',
            '2': 'Gasohol E20',
            '8': 'Hi Diesel B7'
        }
        
        found_count = 0
        for item in items:
            p_id = str(item.get('ProductId', ''))
            if p_id in target_ids:
                price = item.get('Pricetoday')
                if price:
                    message += f"{target_ids[p_id]}: {price} บาท\n"
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
    user_id = 'U9ad765ea3b3a633334cea08ed77d0869' # ไอดีภูริ

    if not token: return

    url = "https://api.line.me/v2/bot/message/push"
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    
    oil_text = get_realtime_oil_prices()
    
    payload = {
        "to": user_id,
        "messages": [{"type": "text", "text": oil_text}]
    }

    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    push_message()
