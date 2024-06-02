import time
import requests
from flask import Flask, jsonify
from datetime import datetime
from threading import Thread

app = Flask(__name__)

URL = 'https://channel-index.onrender.com'  # Replace with your actual URL
status_code = None
last_ping_time = None

@app.route('/')
def home():
    global status_code, last_ping_time
    status_msg = f"Status Code: {status_code}" if status_code else "Ping not started"
    last_ping_msg = f"Last Ping Time: {datetime.fromtimestamp(last_ping_time).strftime('%Y-%m-%d %H:%M:%S')}" if last_ping_time else ""
    return f"Website Pinger Process<br>Status: {status_msg}<br>{last_ping_msg}"

@app.route('/status')
def status():
    next_ping_in = 50 - (time.time() - last_ping_time) if last_ping_time else "Ping not started"
    return jsonify({
        'url': URL,
        'status_code': status_code,
        'last_ping_time': datetime.fromtimestamp(last_ping_time).strftime('%Y-%m-%d %H:%M:%S') if last_ping_time else None,
        'next_ping_in': next_ping_in
    })

def ping_website():
    global status_code, last_ping_time
    while True:
        try:
            response = requests.get(URL)
            status_code = response.status_code
            if response.status_code == 200:
                print(f"Website {URL} is up. Status code: {response.status_code} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"Website {URL} is down. Status code: {response.status_code} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        except requests.RequestException as e:
            print(f"Error pinging website {URL}: {e} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            status_code = 'Error'
        last_ping_time = time.time()
        time.sleep(50)

if __name__ == '__main__':
    thread = Thread(target=ping_website)
    thread.daemon = True
    thread.start()
    app.run(host='0.0.0.0', port=8080)
