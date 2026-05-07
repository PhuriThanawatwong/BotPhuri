import requests
import os

def get_gold_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://api.chnwt.dev/thai-gold-api/latest"
    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            if data.get('status') == 'success':
                return data.get('response', {}).get('price', {}), data.get('response', {}).get('date', '-')
    except:
        pass
    return None, None

def create_flex_message(g, date):
    # นี่คือโครงสร้าง JSON ของ Flex Message ที่จะทำให้หน้าตาเหมือนรูปที่มึงส่งมา
    flex_content = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "💰 ราคาทองคำวันนี้", "weight": "bold", "color": "#1DB446", "size": "xl"},
                {"type": "text", "text": f"อัปเดตล่าสุด: {date}", "size": "xs", "color": "#aaaaaa", "margin": "sm"},
                {"type": "separator", "margin": "xxl"},
                {"type": "box", "layout": "vertical", "margin": "xxl", "spacing": "sm", "contents": [
                    {"type": "box", "layout": "horizontal", "contents": [
                        {"type": "text", "text": "ทองแท่ง (ซื้อ)", "size": "sm", "color": "#555555", "flex": 0},
                        {"type": "text", "text": f"{g.get('gold_bar', {}).get('buy', '-')} บ.", "size": "sm", "color": "#111111", "align": "end", "weight": "bold"}
                    ]},
                    {"type": "box", "layout": "horizontal", "contents": [
                        {"type": "text", "text": "ทองแท่ง (ขาย)", "size": "sm", "color": "#555555", "flex": 0},
                        {"type": "text", "text": f"{g.get('gold_bar', {}).get('sell', '-')} บ.", "size": "sm", "color": "#111111", "align": "end", "weight": "bold"}
                    ]},
                    {"type": "separator", "margin": "md"},
                    {"type": "box", "layout": "horizontal", "margin": "md", "contents": [
                        {"type": "text", "text": "ทองรูปพรรณ (ซื้อ)", "size": "sm", "color": "#555555", "flex": 0},
                        {"type": "text", "text": f"{g.get('gold', {}).get('buy', '-')} บ.", "size": "sm", "color": "#111111", "align": "end", "weight": "bold"}
                    ]},
                    {"type": "box", "layout": "horizontal", "contents": [
                        {"type": "text", "text": "ทองรูปพรรณ (ขาย)", "size": "sm", "color": "#555555", "flex": 0},
                        {"type": "text", "text": f"{g.get('gold', {}).get('sell', '-')} บ.", "size": "sm", "color": "#111111", "align": "end", "weight": "bold"}
                    ]}
                ]},
                {"type": "separator", "margin": "xxl"},
                {"type": "box", "layout": "horizontal", "margin": "md", "contents": [
                    {"type": "text", "text": "BY BOT PHURI", "size": "xs", "color": "#aaaaaa", "flex": 0},
                    {"type": "text", "text": "ECONOMIC ANALYSIS", "color": "#aaaaaa", "size": "xs", "align": "end"}
                ]}
            ]
        }
    }
    return flex_content

def push_message():
    token = os.environ.get('LINE_TOKEN')
    user_id = os.environ.get('USER_ID') or 'U9ad765ea3b3a633334cea08ed77d0869'
    if not token: return
    
    g_data, update_time = get_gold_data()
    if not g_data: return
    
    url = "https://api.line.me/v2/bot/message/push"
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    
    # เปลี่ยนจากส่ง 'text' เป็นส่ง 'flex'
    payload = {
        "to": user_id,
        "messages": [{
            "type": "flex",
            "altText": "รายงานราคาทองคำล่าสุด",
            "contents": create_flex_message(g_data, update_time)
        }]
    }
    
    requests.post(url, headers=headers, json=payload, timeout=10)

if __name__ == "__main__":
    push_message()
