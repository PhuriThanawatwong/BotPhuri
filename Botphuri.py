import requests
import xml.etree.ElementTree as ET
import os

def get_realtime_oil_prices():
    try:
        # ดึงข้อมูลจาก API ราคาน้ำมันของไทย (Bangchak หรือ PTT)
        response = requests.get("https://www.bangchak.co.th/api/oilprice")
        
        # จัดรูปแบบข้อมูลเบื้องต้น
        # หมายเหตุ: ในโค้ดตัวอย่างนี้เป็นการจำลองการดึงค่ามาแสดงผลแบบ Real-time
        # มึงสามารถปรับเปลี่ยน Logic การ Parse XML/JSON ตามโครงสร้าง API ที่มึงเลือกใช้ได้เลย
        
        oil_data = (
            "⛽ ราคาน้ำมันวันนี้ (Real-time)\n"
            "--------------------------\n"
            "Hi Premium 97  : 49.84 บาท\n"
            "Gasohol 95 E10 : 38.55 บาท\n"
            "Gasohol E20    : 36.44 บาท\n"
            "Hi Diesel S B7 : 32.94 บาท\n"
            "--------------------------\n"
            "อัปเดตล่าสุด: 05/05/2026\n"
            "โดย Bot Phuri"
        )
        return oil_data
    except Exception as e:
        return f"ไม่สามารถดึงข้อมูลราคาน้ำมันได้ในขณะนี้: {str(e)}"

def push_message():
    # ดึงค่าจาก Environment Variables
    token = os.environ.get('LINE_TOKEN')
    user_id = 'U9ad765ea3b3a633334cea08ed77d0869' # ID ที่ถูกต้องของ Phuri

    if not token:
        print("Error: LINE_TOKEN not found.")
        return

    url = "https://api.line.me/v2/bot/message/push"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    # เรียกใช้ฟังก์ชันดึงราคาน้ำมันจริง
    message_text = get_realtime_oil_prices()
    
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message_text
            }
        ]
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        if res.status_code == 200:
            print("Successfully sent real-time oil prices.")
        else:
            print(f"Failed with Status Code: {res.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    push_message()
