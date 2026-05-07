import requests
import os

def get_oil_price():
    targets = ["Gasohol 95", "Gasohol E20", "Super Power Gasohol 95", "Diesel B7"]
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        res = requests.get("https://orapiweb.pttor.com/api/oilprice/LatestPrices", headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            message = "⛽ รายงานราคาน้ำมันล่าสุด\n--------------------------\n"
            found = False
            for item in data:
                name = item.get('productName')
                price = item.get('price')
                if name in targets and price:
                    message += f"{name}: {price} บาท\n"
                    found = True
            if found:
                return message + "--------------------------\nระบบรายงานอัตโนมัติ"
    except:
        pass

    try:
        res = requests.get("https://www.bangchak.co.th/api/oilprice", headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            items = data.get('data', {}).get('items', [])
            message = "⛽ รายงานราคาน้ำมันล่าสุด\n--------------------------\n"
            found = False
            bcp_targets = {'1': 'Gasohol 95', '2': 'Gasohol E20', '14': 'Hi Premium 97', '8': 'Hi Diesel B7'}
            for item in items:
                pid = str(item.get('ProductId'))
                price = item.get('Pricetoday') or item.get('Priceyesterday')
                if pid in bcp_targets and price:
                    message += f"{bcp_targets[pid]}: {price} บาท\n"
                    found = True
            if found:
                return message + "--------------------------\nระบบรายงานอัตโนมัติ"
    except:
        pass

    return "⛽ ขออภัย: ระบบไม่สามารถดึงข้อมูลราคาน้ำมันได้ในขณะนี้ โปรดตรวจสอบอีกครั้งภายหลัง"

def push_message():
    token = os.environ.get('LINE_TOKEN')
    user_id = os.environ.get('USER_ID') or 'U9ad765ea3b3a633334cea08ed77d0869'
    if not token:
        return
    oil_text = get_oil_price()
    url = "https://api.line.me/v2/bot/message/push"
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    payload = {"to": user_id, "messages": [{"type": "text", "text": oil_text}]}
    try:
        requests.post(url, headers=headers, json=payload, timeout=10)
    except:
        pass

if __name__ == "__main__":
    push_message()
