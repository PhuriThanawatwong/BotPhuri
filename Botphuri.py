import requests
import os

def get_realtime_oil_prices():
    try:
        # ดึงข้อมูลจาก API บางจาก
        url = "https://www.bangchak.co.th/api/oilprice"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # เข้าถึงชั้นข้อมูล items ที่เก็บรายละเอียดราคาน้ำมัน
            items = data.get('data', {}).get('items', [])
            
            message = "⛽ ราคาน้ำมันวันนี้ (อัปเดตล่าสุด)\n"
            message += "--------------------------\n"
            
            # กำหนด Keyword ที่ใช้ค้นหาและชื่อที่ต้องการแสดงผล
            oil_types = {
                'Premium 97': 'Hi Premium 97',
                '95 E10': 'Gasohol 95',
                'E20': 'Gasohol E20',
                'Diesel S B7': 'Hi Diesel B7'
            }
            
            found_list = []
            for item in items:
                oil_name = item.get('OilName', '')
                for key, display in oil_types.items():
                    if key in oil_name:
                        # ดึงราคาปัจจุบัน
                        price = item.get('Price')
                        if price is not None:
                            found_list.append(f"{display}: {price} บาท")
            
            if found_list:
                message += "\n".join(found_list)
            else:
                message += "ขออภัย กำลังปรับปรุงข้อมูลในระบบ"
                
            message += "\n--------------------------\n"
            message += "รายงานโดย: Bot Phuri"
            return message
        return "❌ ไม่สามารถเชื่อมต่อข้อมูลได้"
    except Exception as e:
        return f"❌ ข้อผิดพลาด: {str(e)}"

def push_message():
    token = os.environ.get('LINE_TOKEN')
    # ยืนยัน ID ผู้ใช้งานที่ถูกต้อง
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
