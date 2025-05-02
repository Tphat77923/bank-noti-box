import requests
import time
import socket
import threading
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
from gtts import gTTS
import os
from datetime import datetime
import subprocess

BASE_URL = "https://my.sepay.vn/userapi"
lim = 10

completed = "Đã nhận thành công số tiền"
ringurl = "https://tiengdong.com/wp-content/uploads/Tieng-ting-www_tiengdong_com.mp3" # URL for the ringtone

if not ringurl:
    ringurl = "ting.mp3" # Default to local file

app = Flask(__name__)

load_dotenv()
API_KEY = os.getenv("API_KEY")
transactions = []
last_transaction_id = None


def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False


def is_api_accessible():
    try:
        response = requests.get(BASE_URL, timeout=3)
        return response.status_code in [200, 401]
    except requests.RequestException:
        return False


def format_amount(amount):
    try:
        amount = float(amount)
        return str(int(amount)) if amount.is_integer() else str(amount)
    except Exception:
        return str(amount)


def get_latest_transactions():
    global transactions, last_transaction_id
    url = f"{BASE_URL}/transactions/list"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"limit": lim, "sort": "desc"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != 200 or "transactions" not in data:
            return

        new_transactions = data["transactions"]
        if not new_transactions:
            return

        now = datetime.now()
        print(now.strftime("[%d/%m/%Y | %H:%M:%S]"), "[✓] API OK")

        new_ids = [tx["id"] for tx in new_transactions]
        if not last_transaction_id:
            last_transaction_id = new_transactions[0]["id"]
            transactions[:] = new_transactions
            return
        if not last_transaction_id or last_transaction_id not in new_ids:
            to_process = reversed(new_transactions)
        else:
            index = new_ids.index(last_transaction_id)
            to_process = reversed(new_transactions[:index])

        for tx in to_process:
            if float(tx.get("amount_in", 0)) > 0:
                notify_transaction(tx)

        last_transaction_id = new_transactions[0]["id"]
        transactions[:] = new_transactions

    except Exception as e:
        print(datetime.now().strftime("[%d/%m/%Y | %H:%M:%S]"),
              f"[!] Lỗi API: {str(e)}")


def notify_transaction(tx):
    try:
        amount = format_amount(tx.get("amount_in", 0))
        message = f"{completed} {amount} đồng."

        print("\n[!] Giao dịch mới!")
        print(f" Ngân hàng: {tx.get('bank_brand_name', 'N/A')}")
        print(f" Số tiền vào: {amount} VND")
        print(f" Thời gian: {tx.get('transaction_date', 'N/A')}")
        print(f" Nội dung: {tx.get('transaction_content', 'N/A')}\n")

        tts = gTTS(text=message, lang="vi")
        tts.save("speech.mp3")

        subprocess.run(["mpv", ringurl, "speech.mp3", "--no-audio-display"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    except Exception as e:
        print(datetime.now().strftime("[%d/%m/%Y | %H:%M:%S]"),
              f"[!] Lỗi khi thông báo: {str(e)}")
    finally:
        if os.path.exists("speech.mp3"):
            try:
                os.remove("speech.mp3")
            except:
                pass


def update_transactions():
    while True:
        try:
            if is_connected() and is_api_accessible():
                get_latest_transactions()
            else:
                print(datetime.now().strftime("[%d/%m/%Y | %H:%M:%S]"),
                      "[?] Mất kết nối, đang thử lại...")
        except Exception as e:
            print(datetime.now().strftime("[%d/%m/%Y | %H:%M:%S]"),
                  f"[!] Lỗi nền: {str(e)}")
        time.sleep(2)


threading.Thread(target=update_transactions, daemon=True).start()


@app.route("/")
def index():
    return render_template("index.html", transactions=transactions)


@app.route("/api/transactions")
def api_transactions():
    return jsonify(transactions)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=False)
