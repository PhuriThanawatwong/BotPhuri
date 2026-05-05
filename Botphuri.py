import requests
import os

def get_realtime_oil_prices():
    try:
        # ดึงข้อมูลจาก API บางจากโดยตรง
        url = "https://www.bangchak.co.th/api/oilprice"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            res_json = response.json()
            items = res_json.get('data', {}).get('items', []) #
            
            message = "⛽ ราคาน้ำมันวันนี้ (อัปเดตล่าสุด)\n"
            message += "--------------------------\n"
            
            # ก๊อปชื่อมาจาก API ของบางจากแบบเป๊ะๆ ทุกตัวอักษร
            oil_targets = {
                'ไฮพรีเมียม 97 แก๊สโซฮอล์ 95++': 'Hi Premium 97',
                'แก๊สโซฮอล์ 95 S EVO': 'Gasohol 95',
                'แก๊สโซฮอล์ E20 S EVO': 'Gasohol E20',
                'ไฮดีเซล S B7': 'Hi Diesel B7'
            }
            
            found_data = []
            for item in items:
                api_name = item.get('OilName', '')
                if api_name in oil_targets:
                    price = item.get('Pricetoday') # ดึงราคาปัจจุบัน
                    if price:
                        found_data.append(f"{oil_targets[api_name]}: {price} บาท")
            
            if found_data:
                message += "\n".join(found_data)
            else:
                message += "ขออภัย กำลังดึงข้อมูลจากระบบบางจาก"
                
            message += "\n--------------------------\n"
            message += "รายงานโดย: Bot Phuri"
            return message
        return "❌ ไม่สามารถเชื่อมต่อ API ได้"
    except Exception as e:
        return f"❌ ข้อผิดพลาด: {str(e)}"

def push_message():
    token = os.environ.get('LINE_TOKEN')
    user_id = 'U9ad765ea3b3a633334cea08ed77d0869' #

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
    push_message()​
