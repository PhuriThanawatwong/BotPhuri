import requests
import os

def get_gold_price():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://api.chnwt.dev/thai-gold-api/latest" 
    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            if data.get('status') == 'success':
                g = data.get('response', {}).get('price', {})
                update_time = data.get('response', {}).get('date', '-')
                msg = f"💰 รายงานราคาทองคำล่าสุด\n📅 {update_time}\n"
                msg += "--------------------------\n"
                msg += f"🏆 ทองแท่ง\nซื้อ: {g.get('gold_bar', {}).get('buy', '-')} | ขาย: {g.get('gold_bar', {}).get('sell', '-')} \n"
                msg += f"💍 ทองรูปพรรณ\nซื้อ: {g.get('gold', {}).get('buy', '-')} | ขาย: {g.get('gold', {}).get('sell', '-')} \n"
                msg += "--------------------------\nระบบรายงานอัตโนมัติ"
                return msg
    except:
        pass
    return "💰 ขออภัย: ระบบ API ทองคำขัดข้อง โปรดลองใหม่อีกครั้ง"

def push_message():
    token = os.environ.get('LINE_TOKEN')
    user_id = os.environ.get('USER_ID') or 'U9ad765ea3b3a633334cea08ed77d0869'
    if not token: return
    oil_text = get_gold_price()
    url = "https://api.line.me/v2/bot/message/push"
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    payload = {"to": user_id, "messages": [{"type": "text", "text": oil_text}]}
    try:
        requests.post(url, headers=headers, json=payload, timeout=10)
    except:
        pass

if __name__ == "__main__":
    push_message()
