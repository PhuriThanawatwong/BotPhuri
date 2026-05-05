import requests
import os

def get_flex_message():
    url = "https://api-v2.bangchak.co.th/api/oilprice"
    try:
        response = requests.get(url, timeout=20)
        data = response.json()
        items = data['data']['items']
        
        oil_list = []
        # เลือกยี่ห้อน้ำมันที่มึงอยากให้โชว์ (เพิ่มได้ตามใจชอบ)
        target = ['Hi Premium 97', 'Gasohol 95 E10', 'Gasohol 91 E10', 'Gasohol E20', 'Hi Diesel S B7']
        
        for item in items:
            if item['type'] in target:
                oil_list.append({
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": item['type'], "size": "sm", "color": "#555555", "flex": 3},
                        {"type": "text", "text": f"{item['price']} บาท", "size": "sm", "weight": "bold", "color": "#111111", "align": "end", "flex": 2}
                    ]
                })

        return {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [{"type": "text", "text": "⛽️ ราคาน้ำมันวันนี้", "weight": "bold", "size": "xl", "color": "#FFFFFF"}],
                "backgroundColor": "#00B900"
            },
            "body": {"type": "box", "layout": "vertical", "contents": oil_list, "spacing": "md"},
            "footer": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "แหล่งข้อมูล: บางจาก", "size": "xs", "color": "#aaaaaa", "align": "center"}]}
        }
    except:
        return None

def broadcast_flex(token):
    flex_content = get_flex_message()
    if not flex_content: return
    
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {"messages": [{"type": "flex", "altText": "เช็คราคาน้ำมัน", "contents": flex_content}]}
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    token = os.getenv('LINE_TOKEN')
    if token:
        broadcast_flex(token)
