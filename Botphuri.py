import requests
import os
import time

def get_oil_price():
    url = "https://api-v2.bangchak.co.th/api/oilprice"
    # ให้มันพยายามดึงข้อมูล 3 รอบ เผื่อเน็ตเน่า
    for i in range(3):
        try:
            response = requests.get(url, timeout=30)
            data = response.json()
            items = data['data']['items']
            msg = "⛽️ รายงานราคาน้ำมันบางจาก\n------------------\n"
            target = ['Hi Premium 97', 'Gasohol 95 E10', 'Gasohol E20', 'Hi Diesel B20']
            for item in items:
                if item['type'] in target:
                    msg += f"🔹 {item['type']}: {item['price']} บาท\n"
            return msg
        except Exception as e:
            if i == 2: # ถ้ารอบที่ 3 ยังไม่ได้ค่อยบอก Error
                return f"❌ ติดต่อ Server ไม่ได้: {str(e)}"
            time.sleep(5) # รอ 5 วิแล้วลองใหม่

def broadcast(token, text):
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {"messages": [{"type": "text", "text": text}]}
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    token = os.getenv('LINE_TOKEN')
    report = get_oil_price()
    if token and report:
        broadcast(token, report)
