import requests
import time
import socket
import threading
from flask import Flask, render_template, jsonify
from gtts import gTTS
import os

BASE_URL = "https://my.sepay.vn/userapi" #api của sepay
API_KEY = "your api key"  # Thay bằng API của bạn
lim = 10 #giới hạn danh sách giao dịch được lấy

#Thông báo nhận thành công
completed = "Đã nhận thành công số tiền"

app = Flask(__name__)


transactions = []
last_transaction_id = None 

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False

def is_api_accessible():
    try:
        response = requests.get(BASE_URL, timeout=5)
        return response.status_code in [200, 401] 
    except requests.RequestException:
        return False

def format_amount(amount):

    amount = float(amount)
    return str(int(amount)) if amount.is_integer() else str(amount)

def get_latest_transactions():
    global transactions, last_transaction_id
    url = f"{BASE_URL}/transactions/list"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"limit": lim, "sort": "desc"} 

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] == 200 and "transactions" in data:
            new_transactions = data["transactions"]
            if not new_transactions: return

            if last_transaction_id and new_transactions[0]["id"] != last_transaction_id:
            	if float(new_transactions[0]["amount_in"]) > 0:
                   notify_transaction(new_transactions[0])

            last_transaction_id = new_transactions[0]["id"]
            transactions = new_transactions
    except requests.RequestException as e:
        print(f"Lỗi API: {str(e)}. Đang thử lại...")

def notify_transaction(tx):
	
    if float(tx["amount_in"]) == 0: return
    message = (
        f"{completed} {format_amount(tx['amount_in'])} đồng. "
    )
    print("\n🔔 Giao dịch mới!")
    print(f"🏦 Ngân hàng: {tx['bank_brand_name']}")
    print(f"💰 Số tiền vào: {format_amount(tx['amount_in'])} VND")
    print(f"📅 Thời gian: {tx['transaction_date']}")
    print(f"📝 Nội dung: {tx['transaction_content']}\n")
    try:
        tts = gTTS(text=message, lang="vi")
        tts.save("speech.mp3")
        os.system("mpv ting.mp3 speech.mp3")
    
        if os.path.exists("speech.mp3"):
            os.remove("speech.mp3")
    except Exception as e:
        print(f"⚠️ Lỗi khi phát âm thanh: {str(e)}")

def update_transactions():
    """ Luồng chạy nền để cập nhật giao dịch mỗi 2 giây """
    while True:
        try:
            if is_connected() and is_api_accessible():
                get_latest_transactions()
            else:
                print("🔴 Mất kết nối, đang kiểm tra lại...")
        except Exception as e:
            print(f"⚠️ Lỗi trong luồng nền: {str(e)}")

        time.sleep(2)

threading.Thread(target=update_transactions, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html", transactions=transactions)

@app.route("/api/transactions")
def api_transactions():
    return jsonify(transactions)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=False)  # Chạy trên cổng 3000
