import os
import requests

def get_air_data():
    api_key = os.environ.get('WEATHER_API_KEY')
    lat, lon = 13.59, 100.95
    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    
    try:
        res = requests.get(url, timeout=20).json()
        pm25 = res['list'][0]['components']['pm2_5']
        
        if pm25 < 15:
            status = "อากาศดีมากครับ 🌿"
        elif pm25 < 37:
            status = "อากาศปานกลางครับ 😷"
        else:
            status = "ค่าฝุ่นสูง ระวังด้วยนะครับ 🛑"
            
        return f"📢 รายงานฝุ่นบางสมัคร\nPM 2.5: {pm25} µg/m³\nสถานะ: {status}"
    except Exception as e:
        return f"Error: {e}"

def send_line(message):
    token = os.environ.get('LINE_TOKEN_AIR')
    user_id = os.environ.get('USER_ID')
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    data = {'to': user_id, 'messages': [{'type': 'text', 'text': message}]}
    requests.post(url, headers=headers, json=data)

if __name__ == "__main__":
    msg = get_air_data()
    send_line(msg)
