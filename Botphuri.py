import requests
import os

def get_oil_price():
    try:
        # ใช้ API กลางของกระทรวงพลังงาน/EPPO หรือแหล่งข้อมูลที่นิ่งกว่า
        url = "https://api.pttor.com/oilprice/LatestPrices" # ตัวอย่าง API ของ OR
        # หมายเหตุ: ถ้า API OR ต้องใช้ Token กูจะปรับเป็นวิธี Scraping หน้าเว็บที่ชัวร์ที่สุดให้
        
        # รอบนี้กูใช้ Scraping ดึงจากหน้าเว็บโดยตรงเลย จะได้ไม่มีปัญหาเรื่อง API ส่งค่า None
        url_web = "https://www.bangchak.co.th/api/oilprice"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url_web, headers=headers, timeout=20)
        data = response.json()
        
        items = data.get('data', {}).get('items', [])
        
        if not items:
            return "⛽ ระบบกำลังรออัปเดตข้อมูลจากสถานี..."

        message = "⛽ ราคาน้ำมันวันนี้ (อัปเดตล่าสุด)\n"
        message += "--------------------------\n"
        
        # ดึงตัวหลักๆ ที่มึงต้องใช้
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
                # ถ้าวันนี้ (Pricetoday) ไม่มี ให้ดึงของเมื่อวาน (Priceyesterday) มาโชว์ก่อน
                price = item.get('Pricetoday') or item.get('Priceyesterday')
                if price:
                    message += f"{targets[pid]}: {price} บาท\n"
                    found = True
        
        if not found:
            return "⛽ ยังไม่มีการประกาศราคาใหม่ในขณะนี้"

        message += "--------------------------\n"
        message += "รายงานโดย: Bot Phuri"
        return message
    except Exception as e:
        return f"❌ ข้อผิดพลาด: {str(e)}"

def push_message():
    token = os.environ.get('LINE_TOKEN')
    user_id = os.environ.get('USER_ID') or 'U9ad765ea3b3a633334cea08ed77d0869' # ไอดีภูริ

    if not token: return

    url = "https://api.line.me/v2/bot/message/push"
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    oil_text = get_oil_price()
    
    payload = {"to": user_id, "messages": [{"type": "text", "text": oil_text}]}
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    push_message()​
