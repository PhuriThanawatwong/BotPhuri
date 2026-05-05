import requests
import os

def get_oil_price():
    # ใช้ API ตรงของบางจาก เสถียรกว่า API รวมที่มึงใช้แล้วล่มอยู่ตอนนี้
    url = "https://api-v2.bangchak.co.th/api/oilprice"
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
        
        # เจาะเข้าโครงสร้างข้อมูลของบางจาก
        items = data['data']['items']
        
        message = "⛽️ ราคาน้ำมันบางจากวันนี้\n"
        message += "------------------\n"
        
        # กรองเอาเฉพาะตัวหลักๆ ที่คนใช้เยอะ
        target_oil = ['Hi Premium 97', 'Gasohol 95 E10', 'Gasohol E20', 'Hi Diesel B20']
        
        for item in items:
            if item['type'] in target_oil:
                name = item['type']
                price = item['price']
                message += f"🔹 {name}: {price} บาท\n"
        
        return message
    except Exception as e:
        # ถ้า Error ให้บอกรายละเอียดชัดๆ จะได้แก้ถูก
        return f"❌ ดึงข้อมูลไม่ได้: {str(e)}"

def broadcast_to_line(token, text_message):
    line_url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Content-Type": "application/json", 
        "Authorization": f"Bearer {token}"
    }
    payload = {"messages": [{"type": "text", "text": text_message}]}
    res = requests.post(line_url, headers=headers, json=payload)
    return res.status_code

# ส่วนรันโปรแกรมบน GitHub Actions
ACCESS_TOKEN = os.getenv('LINE_TOKEN')
report = get_oil_price()

if ACCESS_TOKEN:
    status = broadcast_to_line(ACCESS_TOKEN, report)
    if status == 200:
        print("✅ ส่งข้อมูลเรียบร้อย!")
    else:
        print(f"❌ ส่งไม่สำเร็จ Code: {status}")
else:
    print("⚠️ ไม่พบ LINE_TOKEN (ไปตั้งค่าใน GitHub Secrets ด้วยนะ)")
    print(report)​
