from flask import Flask, request, redirect
import datetime

app = Flask(__name__)

@app.route('/track')
def track_user():
    user_id = request.args.get('user_id', 'unknown')
    phone = request.args.get('phone', 'unknown')

    ua = request.headers.get('User-Agent', '').lower()
    device = ("Android" if "android" in ua else
              "iOS" if "iphone" in ua else
              "Windows" if "windows" in ua else
              "macOS" if "mac" in ua else "Unknown")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"📌 ID: {user_id} | Номер: {phone} | Устройство: {device} | Время: {timestamp}")

    with open('log.txt', 'a') as f:
        f.write(f"{timestamp} | {user_id} | {phone} | {device}\n")

    return redirect("https://example.com", code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
