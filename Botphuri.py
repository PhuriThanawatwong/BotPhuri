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
                
                # ตกแต่งข้อความให้เฟี้ยวขึ้น
                msg =  "✨✨ GOLD REPORT ✨✨\n"
                msg += f"📅 {update_time}\n"
                msg += "━━━━━━━━━━━━━━━\n\n"
                
                msg += "💰 [ ทองคำแท่ง ]\n"
                msg += f"🟢 รับซื้อ : {g.get('gold_bar', {}).get('buy', '-')} ฿\n"
                msg += f"🔴 ขายออก : {g.get('gold_bar', {}).get('sell', '-')} ฿\n\n"
                
                msg += "💍 [ ทองรูปพรรณ ]\n"
                msg += f"🟢 รับซื้อ : {g.get('gold', {}).get('buy', '-')} ฿\n"
                msg += f"🔴 ขายออก : {g.get('gold', {}).get('sell', '-')} ฿\n\n"
                
                msg += "━━━━━━━━━━━━━━━\n"
                msg += "🚀 ระบบวิเคราะห์ข้อมูลอัตโนมัติ"
                return msg
    except:
        pass
    return "❌ ERROR: ไม่สามารถเข้าถึงข้อมูลขุมทรัพย์ได้"

def push_message():
    token = os.environ.get('LINE_TOKEN')
    user_id = os.environ.get('USER_ID') or 'U9ad765ea3b3a633334cea08ed77d0869'
    if not token: return
    
    content = get_gold_price()
    url = "https://api.line.me/v2/bot/message/push"
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    payload = {"to": user_id, "messages": [{"type": "text", "text": content}]}
    
    try:
        requests.post(url, headers=headers, json=payload, timeout=10)
    except:
        pass

if __name__ == "__main__":
    push_message()​
