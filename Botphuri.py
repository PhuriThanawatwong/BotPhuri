import requests
import os

def get_flex_message():
    mock_items = [
        {"type": "Hi Premium 97", "price": "49.84"},
        {"type": "Gasohol 95 E10", "price": "38.55"},
        {"type": "Gasohol E20", "price": "36.44"},
        {"type": "Hi Diesel S B7", "price": "32.94"}
    ]
    oil_contents = []
    for item in mock_items:
        oil_contents.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": item['type'], "size": "sm", "color": "#555555", "flex": 4},
                {"type": "text", "text": item['price'], "size": "sm", "weight": "bold", "color": "#111111", "align": "end", "flex": 2},
                {"type": "text", "text": "บ.", "size": "sm", "color": "#aaaaaa", "align": "end", "flex": 1}
            ]
        })
    return {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://p-u.popcdn.net/attachments/images/000/011/720/large/bangchak.jpg",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "⛽️ ราคาน้ำมันวันนี้", "weight": "bold", "size": "xl", "color": "#024731"},
                {"type": "text", "text": "สถานะ: ข้อมูลทดสอบ (Test)", "size": "xxs", "color": "#ff0000", "margin": "xs"},
                {"type": "box", "layout": "vertical", "margin": "lg", "spacing": "sm", "contents": oil_contents}
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "อัปเดตตี 5 ทุกวัน โดย Bot Phuri", "size": "xs", "color": "#aaaaaa", "align": "center"}
            ]
        }
    }

def broadcast(token):
    flex_content = get_flex_message()
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {"messages": [{"type": "flex", "altText": "Test ราคาน้ำมัน", "contents": flex_content}]}
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    token = os.getenv('LINE_TOKEN')
    if token:
        broadcast(token)
