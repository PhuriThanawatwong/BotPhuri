import requests
import os

def push_message():
    # 1. ดึงกุญแจ (Token) จาก GitHub Secrets ที่มึงตั้งชื่อว่า LINE_TOKEN
    token = os.environ.get('LINE_TOKEN')
    
    # 2. ไอดีของมึงที่กูใส่ให้ตรงๆ ตามที่มึงส่งมาเลยสัส
    user_id = 'U9ad765ea3b3a633334cea08ed77d086'

    if not token:
        print("❌ Error: หา LINE_TOKEN ใน GitHub Secrets ไม่เจอว่ะเพื่อน!")
        return

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
                "text": "เชี่ย... เด้งแล้วววว! ยินดีด้วยสัสภูริ มึงทำสำเร็จแล้วโว้ยยย! 🎉"
            }
        ]
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.text}")
    except Exception as e:
        print(f"❌ พังเพราะ: {e}")

if __name__ == "__main__":
    push_message()
