import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TOR_SOCKS = os.environ.get("TOR_SOCKS", "socks5h://tor:9050")
RANDOMUSER_URL = "https://randomuser.me/api/"

def tor_get(url, params=None, timeout=30):
    proxies = {
        "http": TOR_SOCKS,
        "https": TOR_SOCKS,
    }
    return requests.get(url, params=params, proxies=proxies, timeout=timeout)

@app.get("/api/users")
def get_users():
    results = request.args.get("results", "10")
    try:
        n = int(results)
    except:
        n = 10
    if n < 1:
        n = 1
    if n > 50:
        n = 50

    r = tor_get(RANDOMUSER_URL, params={"results": n})
    r.raise_for_status()
    data = r.json()

    users = []
    for u in data.get("results", []):
        name = u.get("name", {})
        full_name = f"{name.get('first','')} {name.get('last','')}".strip()
        picture = u.get("picture", {}).get("large")
        users.append({
            "name": full_name,
            "photo": picture
        })

    return jsonify(users=users)

@app.get("/api/health")
def health():
    return jsonify(status="ok", tor_socks=TOR_SOCKS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
