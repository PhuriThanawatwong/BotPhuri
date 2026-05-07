def get_oil_price():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        # ลองดึงข้อมูลดิบๆ มาดูเลยว่ามันพ่นอะไรออกมา
        test_res = requests.get("https://orapiweb.pttor.com/api/oilprice/LatestPrices", headers=headers, timeout=10)
        print(f"DEBUG PTT: {test_res.status_code}") # เช็กใน Log GitHub
        
        if test_res.status_code == 200:
            data = test_res.json()
            # ถ้ามีข้อมูลจริง มันต้องไม่ว่าง
            if data:
                message = "⛽ ราคาน้ำมันล่าสุด\n"
                for item in data:
                    if item.get('productName') == "Gasohol 95":
                        message += f"95: {item.get('price')} บาท\n"
                return message + "------------------\nอัปเดตแล้ว!"
    except Exception as e:
        print(f"Error: {e}")
    
    return "⛽ API ยังไม่ปล่อยตัวเลข (เช็ก Log ใน GitHub ด่วนเพื่อน!)"
