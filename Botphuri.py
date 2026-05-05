import requests
import os

def push_message():
    # ดึงค่าจาก GitHub Secrets ที่เราตั้งชื่อไว้ใน main.yml
    token = os.environ.get('LINE_TOKEN')
    user_id = os.environ.get('USER_ID')

    if not token or not user_id:
        print("❌ Error: หา LINE_TOKEN หรือ USER_ID ไม่เจอในระบบสัส!")
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
                "text": "สำเร็จแล้วสัสภูริ! เลิกเขียวหลอกๆ แล้วเด้งจริงซะที! ยินดีด้วยไอ้ชาย!"
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
