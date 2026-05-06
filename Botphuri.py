import requests
import os

def get_realtime_oil_prices():
    try:
        url = "https://www.bangchak.co.th/api/oilprice"
        response = requests.get(url, timeout=15)
        res_data = response.json()
        
        # ลอง print ดูในหน้า Actions ว่าข้อมูลมาจริงไหม
        print(f"DEBUG API Response: {res_data}")
        
        items = res_data.get('data', {}).get('items', [])
        
        if not items:
            return "⛽ กำลังรอข้อมูลราคาจากหน้าสถานี (API Data Empty)"
        
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
                price = item.get('Pricetoday')
                # เช็กถ้าราคาเป็น None หรือ String ว่าง
                if price and str(price).strip():
                    message += f"{target_ids[p_id]}: {price} บาท\n"
                    found_count += 1
        
        if found_count == 0:
            return "⛽ กำลังรอข้อมูลราคาจากหน้าสถานี (No Price Found)"
            
        message += "--------------------------\n"
        message += "รายงานโดย: Bot Phuri"
        return message
    except Exception as e:
        print(f"DEBUG Error: {str(e)}")
        return f"❌ ข้อผิดพลาด: {str(e)}"

def push_message():
    token = os.environ.get('LINE_TOKEN')
    user_id = 'U9ad765ea3b3a633334cea08ed77d0869' # ไอดีภูริ

    if not token: 
        print("DEBUG: No LINE_TOKEN found")
        return

    url = "https://api.line.me/v2/bot/message/push"
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    
    oil_text = get_realtime_oil_prices()
    
    payload = {
        "to": user_id,
        "messages": [{"type": "text", "text": oil_text}]
    }

    res = requests.post(url, headers=headers, json=payload)
    print(f"DEBUG LINE Status: {res.status_code}")

if __name__ == "__main__":
    push_message()
