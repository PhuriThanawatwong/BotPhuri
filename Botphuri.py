import requests
import os
import re

def get_gold_price():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://thai-gold-api.vercel.app/latest" # แหล่งข้อมูลราคาทองสมาคมฯ
    
    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            # ดึงข้อมูลจาก JSON (โครงสร้างของสมาคมค้าทองคำ)
            gold_bar = data.get('response', {}).get('gold_bar', {})
            gold_ornament = data.get('response', {}).get('gold', {})
            update_time = data.get('response', {}).get('date', 'ไม่ระบุเวลา')

            message = f"💰 รายงานราคาทองคำวันนี้\n📅 {update_time}\n"
            message += "--------------------------\n"
            message += f"🏆 ทองแท่ง\nรับซื้อ: {gold_bar.get('buy', '-')} บาท\nขายออก: {gold_bar.get('sell', '-')} บาท\n\n"
            message += f"💍 ทองรูปพรรณ\nรับซื้อ: {gold_ornament.get('buy', '-')} บาท\nขายออก: {gold_ornament.get('sell', '-')} บาท\n"
            message += "--------------------------\nระบบรายงานอัตโนมัติ"
            return message
    except Exception as e:
        print(f"Error: {e}")
        pass

    return "💰 ขออภัย: ไม่สามารถดึงข้อมูลราคาทองได้ในขณะนี้"

def push_message():
    token = os.environ.get('LINE_TOKEN')
    # ใช้ USER_ID จาก Secret หรือค่า Default (เช็กให้ตรงกับของมึงนะสัส)
    user_id = os.environ.get('USER_ID') or 'U9ad765ea3b3a633334cea08ed77d0869'
    
    if not token:
        print("Error: LINE_TOKEN not found")
        return
        
    text_content = get_gold_price()
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    payload = {
        "to": user_id,
        "messages": [{"type": "text", "text": text_content}]
    }
    
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"Status: {r.status_code}")
    except Exception as e:
        print(f"Send Error: {e}")

if __name__ == "__main__":
    push_message()
