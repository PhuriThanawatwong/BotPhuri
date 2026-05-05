import requests
import os

def get_oil_price():
    # ลองดึงของจริงดูก่อน
    url = "https://api-v2.bangchak.co.th/api/oilprice"
    try:
        response = requests.get(url, timeout=20)
        data = response.json()
        items = data['data']['items']
        msg = "⛽️ ราคาน้ำมันบางจากวันนี้ (อัปเดตแล้ว)\n------------------\n"
        target = ['Hi Premium 97', 'Gasohol 95 E10', 'Gasohol E20', 'Hi Diesel B20']
        for item in items:
            if item['type'] in target:
                msg += f"🔹 {item['type']}: {item['price']} บาท\n"
        return msg
    except:
        # ถ้าดึงไม่ได้ ให้ส่งข้อความเทสไปเลย จะได้รู้ว่าบอทไม่ตาย
        return "⛽️ ราคาน้ำมันบางจาก (ระบบสำรอง)\n------------------\n🔹 Gasohol 95: 38.55 บาท\n🔹 Gasohol E20: 36.44 บาท\n⚠️ หมายเหตุ: ข้อมูลนี้เป็นชุดทดสอบ"

def broadcast(token, text):
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {"messages": [{"type": "text", "text": text}]}
    res = requests.post(url, headers=headers, json=payload)
    print(f"Status: {res.status_code}")

if __name__ == "__main__":
    token = os.getenv('LINE_TOKEN')
    report = get_oil_price()
    if token:
        broadcast(token, report)
