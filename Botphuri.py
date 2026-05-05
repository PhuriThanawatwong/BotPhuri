import requests
import os

def broadcast_test(token):
    # ยิงข้อความตรงๆ เข้า LINE เพื่อเช็คว่า Token ยังขลังอยู่มั้ย
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    # ลองดึงราคาน้ำมันจริง
    try:
        res_oil = requests.get("https://api-v2.bangchak.co.th/api/oilprice", timeout=15)
        data = res_oil.json()
        items = data['data']['items']
        msg = "⛽️ ราคาน้ำมันมาแล้วเว้ยภูริ!\n"
        for item in items[:5]: # เอามาโชว์ 5 ตัวพอเป็นพิธี
            msg += f"🔹 {item['type']}: {item['price']} บาท\n"
    except Exception as e:
        msg = f"⚠️ ดึงราคาไม่ได้แต่บอทยังไม่ตายนะ: {str(e)}"

    payload = {"messages": [{"type": "text", "text": msg}]}
    response = requests.post(url, headers=headers, json=payload)
    print(f"LINE Response: {response.status_code} - {response.text}")

if __name__ == "__main__":
    token = os.getenv('LINE_TOKEN')
    if token:
        broadcast_test(token)
    else:
        print("❌ มึงลืมใส่ LINE_TOKEN ใน GitHub Secrets หรือเปล่า?")
