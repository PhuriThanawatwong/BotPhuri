import requests

def get_oil_prices():
    # เปลี่ยนมาใช้ API กลางที่ดึงได้ทุกปั๊ม (ตัวอย่าง URL ที่เสถียรกว่า)
    url = "https://api.sumup.in.th/oil/latest" 
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data
        return None
    except:
        return None

def send_line_message(data):
    token = "ใส่_LINE_TOKEN_ของมึงตรงนี้" # หรือใช้จาก Env แบบที่มึงทำใน GitHub
    url = "https://notify-api.line.me/api/notify"
    
    # ดึงราคาแต่ละเจ้า (ปรับตามโครงสร้าง JSON ใหม่)
    # สมมติเราดึงราคาเฉลี่ยหรือราคาเจ้าหลักๆ มาโชว์
    msg = "\n⛽️ รายงานราคาน้ำมันทุกปั๊มวันนี้\n"
    
    # วนลูปดึงข้อมูลที่ได้มา
    for station in data['stations']:
        msg += f"\n📍 {station['name']}:"
        for oil in station['prices']:
            msg += f"\n- {oil['type']}: {oil['price']} บาท"
        msg += "\n"

    headers = {'Authorization': f'Bearer {token}'}
    res = requests.post(url, headers=headers, data={'message': msg})
    return res.status_code

# รันระบบ
oil_data = get_oil_prices()
if oil_data:
    status = send_line_message(oil_data)
    print(f"ส่งข้อมูลสำเร็จ: {status}")
else:
    print("ดึงข้อมูลไม่ได้ สงสัย Server ล่มหมดประเทศสัส!")
