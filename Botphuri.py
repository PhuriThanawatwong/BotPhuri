import requests
import os

def push_message():
    # 1. กุญแจ (Token) ดึงจากที่มึงตั้งไว้ใน GitHub
    token = os.environ.get('LINE_TOKEN') 
    
    # 2. ไอดีมึง (กูใส่ให้ตรงๆ เลยสัส จะได้ไม่พลาด) 
    # เอาเลขที่ขึ้นต้นด้วย U9ad76... จากหน้า Basic Settings มาใส่ตรงนี้แทนคำว่า 'ไอดีมึง'
    user_id = os.environ.get('USER_ID') or 'U9ad765ea673449d0124e548873099999' # ใส่ ID จริงมึงลงไปในเครื่องหมายคำพูดเลยก็ได้

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
                "text": "สำเร็จแล้วสัสภูริ! เลิกเขียวหลอกๆ แล้วเด้งจริงซะที!"
            }
        ]
    }

    res = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {res.status_code}")
    print(f"Response: {res.text}")

push_message()
