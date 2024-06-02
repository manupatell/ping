import time
import requests
from flask import Flask, jsonify
from datetime import datetime, timedelta
from threading import Thread

app = Flask(__name__)

URL = 'https://channel-index.onrender.com/login'
status_code = None
last_ping_time = None
time_zone_offset = timedelta(hours=5, minutes=30)

def get_local_time(utc_time):
    if utc_time:
        local_time = utc_time + time_zone_offset
        return local_time.strftime('%Y-%m-%d %H:%M:%S')
    return None

@app.route('/')
def home():
    return "Welcome to the Website Pinger!"

@app.route('/status')
def status():
    global status_code, last_ping_time
    status_msg = f"Status Code: {status_code}" if status_code else "Ping not started"
    last_ping_msg = f"Last Ping Time: {get_local_time(last_ping_time)}" if last_ping_time else ""
    return f"Website Pinger Process<br>Status: {status_msg}<br>{last_ping_msg}"

def ping_website():
    global status_code, last_ping_time
    while True:
        try:
            response = requests.get(URL)
            status_code = response.status_code
            if response.status_code == 200:
                print(f"Website {URL} is up. Status code: {response.status_code} at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
            else:
                print(f"Website {URL} is down. Status code: {response.status_code} at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        except requests.RequestException as e:
            print(f"Error pinging website {URL}: {e} at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
            status_code = 'Error'
        last_ping_time = datetime.utcnow()
        time.sleep(50)

if __name__ == '__main__':
    # Start the ping process immediately
    ping_thread = Thread(target=ping_website)
    ping_thread.daemon = True
    ping_thread.start()

    # Start the Flask app
    app.run(host='0.0.0.0', port=8080)
