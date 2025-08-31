# server.py
from flask import Flask, request, redirect
import datetime
import json
import requests

app = Flask(__name__)

# 🌐 Целевой сайт
TARGET_SITE = "https://example.com"  # ← Замените на нужный

# Функция для получения геолокации по IP
def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = response.json()
        if data['status'] == 'success':
            return {
                'country': data.get('country', 'unknown'),
                'city': data.get('city', 'unknown'),
                'isp': data.get('isp', 'unknown')
            }
        else:
            return {'country': 'unknown', 'city': 'unknown', 'isp': 'unknown'}
    except:
        return {'country': 'unknown', 'city': 'unknown', 'isp': 'unknown'}

@app.route('/track')
def track_user():
    # Параметры из ссылки
    user_id = request.args.get('user_id', 'unknown')
    phone = request.args.get('phone', 'unknown')

    # User-Agent
    ua = request.headers.get('User-Agent', 'unknown').lower()
    referrer = request.headers.get('Referer', 'unknown')
    language = request.headers.get('Accept-Language', 'unknown')

    # Определяем устройство
    if 'android' in ua:
        device = 'Android'
        os = 'Android'
    elif 'iphone' in ua or 'ipad' in ua:
        device = 'iOS'
        os = 'iOS'
    elif 'windows' in ua:
        device = 'Windows PC'
        os = 'Windows'
    elif 'mac' in ua and 'iphone' not in ua:
        device = 'Mac'
        os = 'macOS'
    elif 'linux' in ua:
        device = 'Linux PC'
        os = 'Linux'
    else:
        device = 'Unknown'
        os = 'Unknown'

    # Определяем браузер
    browser = 'Unknown'
    if 'edg' in ua:
        browser = 'Edge'
    elif 'chrome' in ua and 'edg' not in ua:
        browser = 'Chrome'
    elif 'firefox' in ua:
        browser = 'Firefox'
    elif 'safari' in ua and 'chrome' not in ua:
        browser = 'Safari'
    elif 'opr' in ua or 'opera' in ua:
        browser = 'Opera'

    # Время
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # IP-адрес
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        ip = request.remote_addr

    # Геолокация
    location = get_location(ip)

    # Собираем все данные
    log_data = {
        "timestamp": timestamp,
        "user_id": user_id,
        "phone": phone,
        "ip": ip,
        "device": device,
        "os": os,
        "browser": browser,
        "language": language,
        "referrer": referrer,
        "country": location['country'],
        "city": location['city'],
        "isp": location['isp'],
        "user_agent": ua
    }

    # Логируем в консоль
    print(f"📌 [TRACK] {json.dumps(log_data, ensure_ascii=False)}")

    # Сохраняем в файл
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_data, ensure_ascii=False) + '\n')

    # Перенаправляем
    return redirect(TARGET_SITE, code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
