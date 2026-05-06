import requests
import os

def get_realtime_oil_prices():
    try:
        url = "https://www.bangchak.co.th/api/oilprice"
        response = requests.get(url, timeout=20)
        res_data = response.json()
        items = res_data.get('data', {}).get('items', [])
        
        if not items:
            return "⛽ รอข้อมูลจากสถานี (API Empty)"
        
        message = "⛽ ราคาน้ำมันวันนี้ (อัปเดตล่าสุด)\n"
        message += "--------------------------\n"
        
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
                # พยายามดึงราคาจากทุกช่องที่มีความเป็นไปได้
                price = item.get('Pricetoday') or item.get('Priceyesterday') or item.get('Price')
                
                if price and str(price) not in ["0", "0.0", "None"]:
                    message += f"{target_ids[p_id]}: {price} บาท\n"
                    found_count += 1
        
        if found_count == 0:
            return "⛽ API ยังไม่ปล่อยราคา (ลองเช็กอีกทีช่วงเช้ามืด)"
            
        message += "--------------------------\n"
        message += "รายงานโดย: Bot Phuri"
        return message
    except Exception as e:
        return f"❌ ข้อผิดพลาด: {str(e)}"

def push_message():
    token = os.environ.get('LINE_TOKEN')
    user_id = os.environ.get('USER_ID') or 'U9ad765ea3b3a633334cea08ed77d0869'

    if not token: return

    url = "https://api.line.me/v2/bot/message/push"
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    oil_text = get_realtime_oil_prices()
    
    payload = {"to": user_id, "messages": [{"type": "text", "text": oil_text}]}
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    push_message()
