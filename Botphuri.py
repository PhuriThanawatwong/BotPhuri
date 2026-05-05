import requests

def get_oil_price():
    url = "https://api-v2.bangchak.co.th/api/oilprice"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        items = data['data']['items']
        message = "⛽️ รายงานราคาน้ำมันวันนี้\n"
        message += "------------------\n"
        for item in items:
            message += f"🔹 {item['type']}: {item['price']} บาท\n"
        return message # <--- ตรงนี้ต้องย่อหน้าเข้ามาให้ตรงกับ for
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {e}"

def broadcast_to_line(token, text_message):
    line_url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "messages": [{"type": "text", "text": text_message}]
    }
    response = requests.post(line_url, headers=headers, json=payload)
    if response.status_code == 200:
        print("✅ ส่งข่าวสำเร็จ!")
    else:
        print(f"❌ พลาด: {response.status_code}")

# --- ใส่ Token ของมึงตรงนี้ ---
ACCESS_TOKEN =" CXxbZo3WrtD73N7L/o3t8gGOv6rxjZdt/boMGbQmd1s8A8dW3+D1E1Q+aq4ZZi0vU+kekbD3H+RFZhtG33QLgzf2SdCrB/sRshcmKhZjPpJ9myOY2GhUxmCpWTntVsQo+m/v5bSrUSMoI3WphQGURAdB04t89/1O/w1cDnyilFU="

# รันโปรแกรม
report = get_oil_price()
broadcast_to_line(ACCESS_TOKEN
