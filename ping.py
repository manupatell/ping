# ping.py
import time
import requests
from flask import Flask

app = Flask(__name__)

URL = 'https://channel-index.onrender.com'  # Replace with your actual URL

@app.route('/')
def home():
    return "Website Pinger is Running"

def ping_website():
    while True:
        try:
            response = requests.get(URL)
            if response.status_code == 200:
                print(f"Website {URL} is up. Status code: {response.status_code}")
            else:
                print(f"Website {URL} is down. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error pinging website {URL}: {e}")
        time.sleep(50)

if __name__ == '__main__':
    from threading import Thread
    thread = Thread(target=ping_website)
    thread.daemon = True
    thread.start()
    app.run(host='0.0.0.0', port=8000)
