import requests
import os

def get_oil_prices():
    # ใช้ API จากแหล่งอื่นที่เสถียร (หรือลองเปลี่ยนกลับมาบางจากถ้าเขาซ่อมเสร็จ)
    url = "https://api.sumup.in.th/oil/latest" 
    try:
        response = requests.get(url, timeout=15)
        print(f"API Response Status: {response.status_code}") # เช็คว่า API ตอบกลับมั้ย
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def send_line(message_text):
    # ใช้ Token ที่มึงตั้งไว้ใน GitHub Secrets (แนะนำให้ใช้ชื่อ LINE_TOKEN)
    token = os.environ.get('LINE_TOKEN') 
    if not token:
        print("Error: ไม่เจอ LINE_TOKEN ใน GitHub Secrets สัส!")
        return
        
    url = "https://notify-api.line.me/api/notify"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        res = requests.post(url, headers=headers, data={'message': message_text})
        print(f"LINE Notify Status: {res.status_code}") # ถ้าขึ้น 200 คือเด้งชัวร์
        return res.status_code
    except Exception as e:
        print(f"Error sending to LINE: {e}")

# --- เริ่มทำงาน ---
data = get_oil_prices()

if data:
    # ลองส่งข้อความแบบง่ายๆ ไปก่อนเพื่อเช็คว่า LINE เชื่อมติดมั้ย
    test_msg = "\n🤖 Botphuri Report\nดึงข้อมูลสำเร็จแล้วเพื่อน!"
    send_line(test_msg)
    
    # ถ้าอยากดูข้อมูลดิบที่ดึงมาได้ ให้ปลดล็อคบรรทัดข้างล่างนี้
    # print(data) 
else:
    print("ดึงข้อมูลไม่ได้เลยสัส ลองเช็ค URL API อีกที!")
