import requests
import os

def get_flex_message():
    url = "https://api-v2.bangchak.co.th/api/oilprice"
    try:
        response = requests.get(url, timeout=20)
        data = response.json()
        items = data['data']['items']
        
        oil_list = []
        target = ['Hi Premium 97', 'Gasohol 95 E10', 'Gasohol E20', 'Hi Diesel S B7']
        
        for item in items:
            if item['type'] in target:
                oil_list.append({
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": item['type'], "size": "sm", "color": "#555555", "flex": 4},
                        {"type": "text", "text": f"{item['price']}", "size": "sm", "weight": "bold", "color": "#111111", "align": "end", "flex": 2},
                        {"type": "text", "text": "บ.", "size": "sm", "color": "#aaaaaa", "align": "end", "flex": 1}
                    ]
                })

        return {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://p-u.popcdn.net/attachments/images/000/011/720/large/bangchak.jpg",
                "size": "full", "aspectRatio": "20:13", "aspectMode": "cover"
            },
            "body": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "⛽️ ราคาน้ำมันวันนี้", "weight": "bold", "size": "xl", "color": "#024731"},
                    {"type": "box", "layout": "vertical", "margin": "lg", "spacing": "sm", "contents": oil_list}
                ]
            },
            "footer": {
                "type": "box", "layout": "vertical",
                "contents": [{"type": "text", "text": "อัปเดตตี 5 ทุกวัน โดย Bot Phuri", "size": "xs", "color": "#aaaaaa", "align": "center"}]
            }
        }
    except:
        return None

def broadcast(token):
    flex_content = get_flex_message()
    if not flex_content: return
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {"messages": [{"type": "flex", "altText": "เช็คราคาน้ำมันวันนี้", "contents": flex_content}]}
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    token = os.getenv('LINE_TOKEN')
    if token:
        broadcast(token)
