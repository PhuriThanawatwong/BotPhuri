import os
import requests

def get_air_data():
    api_key = os.environ.get('WEATHER_API_KEY')
    lat, lon = 13.59, 100.95 # บางสมัคร
    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    
    try:
        res = requests.get(url, timeout=20).json()
        pm25 = res['list'][0]['components']['pm2_5']
        
        if pm25 < 15:
            icon, status = "🍏", "อากาศดีมาก สดชื่นสุดๆ"
        elif pm25 < 37:
            icon, status = "🍊", "อากาศปานกลาง ระวังด้วยครับ"
        else:
            icon, status = "🛑", "ค่าฝุ่นสูง อย่าลืมสวมหน้ากาก"
            
        msg =  "☁️ รายงานฝุ่นบางสมัคร (PM 2.5)\n"
        msg += "━━━━━━━━━━━━━━\n"
        msg += f"📊 ค่าฝุ่น : {pm25} µg/m³\n"
        msg += f"🌡️ สถานะ : {status} {icon}\n"
        msg += "━━━━━━━━━━━━━━\n"
        msg += "ดูแลสุขภาพด้วยนะครับทุกคน ✨"
        return msg
    except:
        return "⚠️ ระบบตรวจสอบอากาศขัดข้อง"

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
