import requests
import os

def get_oil_price():
    url = "https://api-v2.bangchak.co.th/api/oilprice"
    try:
        response = requests.get(url, timeout=20)
        data = response.json()
        items = data['data']['items']
        msg = "⛽️ ราคาน้ำมันบางจากวันนี้\n"
        msg += "------------------\n"
        target = ['Hi Premium 97', 'Gasohol 95 E10', 'Gasohol E20', 'Hi Diesel B20']
        for item in items:
            if item['type'] in target:
                msg += f"🔹 {item['type']}: {item['price']} บาท\n"
        return msg
    except Exception as e:
        return f"Error: {str(e)}"

def broadcast(token, text):
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {"messages": [{"type": "text", "text": text}]}
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    token = os.getenv('LINE_TOKEN')
    report = get_oil_price()
    if token:
        broadcast(token, report)
        print("Done")
    else:
        print("No Token found")​
