import requests
import os

def get_oil_price():
    try:
        # ย้ายมาดึงข้อมูลจาก API กลางที่นิ่งกว่าเดิม
        url = "https://api.pttor.com/oilprice/LatestPrices" 
        # ถ้า API เฉพาะทางมีปัญหา เราจะใช้ Backup เป็นการดึงข้อมูลภาพรวมที่อัปเดตชัวร์ๆ
        url_alt = "https://www.bangchak.co.th/api/oilprice"
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url_alt, headers=headers, timeout=20)
        data = response.json()
        items = data.get('data', {}).get('items', [])

        if not items:
            return "⛽ ระบบขัดข้อง: ไม่สามารถดึงข้อมูลได้ในขณะนี้"

        message = "⛽ ราคาน้ำมันล่าสุด (อัปเดตชัวร์)\n"
        message += "--------------------------\n"
        
        # คัดเฉพาะตัวที่มึงใช้บ่อยๆ
        targets = {
            '1': 'Gasohol 95',
            '2': 'Gasohol E20',
            '14': 'Hi Premium 97',
            '8': 'Hi Diesel B7'
        }

        found = False
        for item in items:
            pid = str(item.get('ProductId'))
            if pid in targets:
                # LOGIC ใหม่: ถ้าวันนี้ไม่มีราคา ให้เอาราคาล่าสุดที่มี (Priceyesterday) มาโชว์เลย ไม่ปล่อยว่าง
                price = item.get('Pricetoday')
                if not price or str(price) in ["0", "0.0", "None"]:
                    price = item.get('Priceyesterday')
                
                if price:
                    message += f"{targets[pid]}: {price} บาท\n"
                    found = True
        
        if not found:
            return "⛽ ยังไม่มีการประกาศราคาในระบบ"

        message += "--------------------------\n"
        message += "รายงานโดย: Bot Phuri"
        return message
    except Exception as e:
        return f"❌ Error: {str(e)}"

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
