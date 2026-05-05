import requests
import os

def get_oil_price():
    # แหล่งที่ 1: บางจาก
    try:
        res = requests.get("https://api-v2.bangchak.co.th/api/oilprice", timeout=10)
        items = res.json()['data']['items']
        msg = "⛽️ ราคาน้ำมันวันนี้ (บางจาก)\n------------------\n"
        for item in items[:5]:
            msg += f"🔹 {item['type']}: {item['price']} บาท\n"
        return msg
    except:
        # แหล่งที่ 2: ปตท. (ถ้าบางจากล่ม)
        try:
            res = requests.get("https://api.chnwt.dev/thai-oil-api/latest", timeout=10)
            ptt = res.json()['price']['ptt']
            msg = "⛽️ ราคาน้ำมันวันนี้ (ปตท.)\n------------------\n"
            for k, v in ptt.items():
                if v: msg += f"🔹 {k}: {v} บาท\n"
            return msg
        except:
            return "⛽️ ระบบดึงราคาน้ำมันขัดข้องทั้งคู่ กรุณาลองใหม่ภายหลัง"

def broadcast(token):
    msg = get_oil_price()
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {"messages": [{"type": "text", "text": msg}]}
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    token = os.getenv('LINE_TOKEN')
    if token:
        broadcast(token)
