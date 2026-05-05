import requests
import os

def get_flex_message():
    # ดึงข้อมูลจากบางจาก
    url = "https://api-v2.bangchak.co.th/api/oilprice"
    try:
        response = requests.get(url, timeout=20)
        data = response.json()
        items = data['data']['items']
        
        oil_contents = []
        # เลือกตัวหลักๆ มาโชว์
        target = ['Hi Premium 97', 'Gasohol 95 E10', 'Gasohol E20', 'Hi Diesel S B7']
        
        for item in items:
            if item['type'] in target:
                oil_contents.append({
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": item['type'], "size": "sm", "color": "#555555", "flex": 4},
                        {"type": "text", "text": f"{item['price']}", "size": "sm", "weight": "bold", "color": "#111111", "align": "end", "flex": 2},
                        {"type": "text", "text": "บ.", "size": "sm", "color": "#aaaaaa", "align": "end", "flex": 1}
                    ]
                })

        # โครงสร้าง Flex Message แบบใส่รูปและสี
        return {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://www.bangchak.co.th/assets/images/logo.png",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "⛽️ ราคาน้ำมันวันนี้", "weight": "bold", "size": "xl"},
                    {"type": "box", "layout": "vertical", "margin": "lg", "spacing": "sm", "contents": oil_contents}
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "อัปเดตตี 5 ทุกวัน", "size": "xs", "color": "#aaaaaa", "align": "center"}
                ]
            }
        }
    except:
        # ถ้าดึงไม่ได้ ให้ส่ง Flex แบบ Error ไปแทน (จะได้รู้ว่าบอทไม่ตาย)
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [{"type": "text", "text": "⚠️ ระบบดึงข้อมูลขัดข้อง", "color": "#ff0000"}]
            }
        }

def broadcast(token):
    flex_content = get_flex_message()
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "messages": [{
            "type": "flex",
            "altText": "เช็คราคาน้ำมันวันนี้",
            "contents": flex_content
        }]
    }
    res = requests.post(url, headers=headers, json=payload)
    print(f"Status: {res.status_code}")

if __name__ == "__main__":
    token = os.getenv('LINE_TOKEN')
    if token:
        broadcast(token)
