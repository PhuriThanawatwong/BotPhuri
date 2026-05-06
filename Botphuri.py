import requests
import os

def get_oil_price():
    try:
        url = "https://www.bangchak.co.th/api/oilprice"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=20)
        data = response.json()
        items = data.get('data', {}).get('items', [])
        if not items:
            return "⛽ รอข้อมูลจากสถานี"
        message = "⛽ ราคาน้ำมันวันนี้\n"
        message += "--------------------------\n"
        targets = {'1': 'Gasohol 95', '2': 'Gasohol E20', '14': 'Hi Premium 97', '8': 'Hi Diesel B7'}
        found = False
        for item in items:
            pid = str(item.get('ProductId'))
            if pid in targets:
                price = item.get('Pricetoday') or item.get('Priceyesterday')
                if price and str(price) not in ["0", "0.0", "None"]:
                    message += f"{targets[pid]}: {price} บาท\n"
                    found = True
        if not found:
            return "⛽ ยังไม่มีประกาศราคาใหม่"
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
    oil_text = get_oil_price()
    payload = {"to": user_id, "messages": [{"type": "text", "text": oil_text}]}
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    push_message()
