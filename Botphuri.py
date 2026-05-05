import requests
import os

def push_message():
    # ดึงค่าจาก GitHub Secrets ที่มึงต้องไปตั้งชื่อให้ตรงกันนะเพื่อน
    token = os.environ.get('LINE_TOKEN') 
    user_id = os.environ.get('USER_ID') 

    url = "https://api.line.me/v2/bot/message/push"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": "เฮ้ยภูริ! ถ้ามึงเห็นอันนี้แปลว่า Messaging API ของจริงเด้งแล้วสัส! โค้ดมึงผ่านแล้ว!"
            }
        ]
    }

    res = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {res.status_code}")
    print(f"Response: {res.text}")

push_message()
