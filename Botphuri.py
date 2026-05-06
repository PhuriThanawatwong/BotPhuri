import requests
import os

def get_oil_price():
    # รายชื่อน้ำมันที่มึงต้องใช้
    targets = ["Gasohol 95", "Gasohol E20", "Super Power Gasohol 95", "Diesel B7"]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    # --- LAYER 1: พยายามดึงจาก OR (แหล่งที่นิ่งที่สุด) ---
    try:
        res = requests.get("https://orapiweb.pttor.com/api/oilprice/LatestPrices", headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            message = "⛽ ราคาน้ำมันล่าสุด (PTT)\n--------------------------\n"
            found = False
            for item in data:
                name = item.get('productName')
                price = item.get('price')
                if name in targets and price:
                    message += f"{name}: {price} บาท\n"
                    found = True
            if found:
                return message + "--------------------------\nรายงานโดย: Bot Phuri"
    except:
        pass # ถ้า Layer 1 พัง ให้ข้ามไป Layer 2 ทันที

    # --- LAYER 2: พยายามดึงจาก Bangchak (แหล่งสำรอง) ---
    try:
        res = requests.get("https://www.bangchak.co.th/api/oilprice", headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            items = data.get('data', {}).get('items', [])
            message = "⛽ ราคาน้ำมันล่าสุด (BCP)\n--------------------------\n"
            found = False
            # แมพ ID ของบางจากให้ตรงกับชื่อที่มึงเข้าใจ
            bcp_targets = {'1': 'Gasohol 95', '2': 'Gasohol E20', '14': 'Hi Premium 97', '8': 'Hi Diesel B7'}
            for item in items:
                pid = str(item.get('ProductId'))
                price = item.get('Pricetoday') or item.get('Priceyesterday')
                if pid in bcp_targets and price:
                    message += f"{bcp_targets[pid]}: {price} บาท\n"
                    found = True
            if found:
                return message + "--------------------------\nรายงานโดย: Bot Phuri"
    except:
        pass

    return "⛽ ขออภัยเพื่อนภูริ: ระบบต้นทางปิดปรับปรุงข้อมูลชั่วคราว"

def push_message():
    token = os.environ.get('LINE_TOKEN')
    user_id = os.environ.get('USER_ID') or 'U9ad765ea3b3a633334cea08ed77d0869'
    if not token: return
    
    oil_text = get_oil_price()
    url = "https://api.line.me/v2/bot/message/push"
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    payload = {"to": user_id, "messages": [{"type": "text", "text": oil_text}]}
    
    try:
        requests.post(url, headers=headers, json=payload, timeout=10)
    except Exception as e:
        print(f"Push Error: {e}")

if __name__ == "__main__":
    push_message()
