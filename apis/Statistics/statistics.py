import os
from flask import Flask, request, jsonify
import psycopg2
import requests

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
DEVICE_REG_URL = os.getenv("DEVICE_REGISTRATION_URL", "http://localhost:8081")

ALLOWED = {"iOS", "Android", "Watch", "TV"}

@app.get("/healthz")
def healthz():
    return "ok", 200

@app.post("/Log/auth")
def log_auth():
    try:
        data = request.get_json() or {}
        user_key = (data.get("userKey") or "").strip()
        device_type = data.get("deviceType") or ""

        if user_key == "" or device_type not in ALLOWED:
            return jsonify(statusCode=400, message="bad_request"), 400

        r = requests.post(
            f"{DEVICE_REG_URL}/Device/Register",
            json={"userKey": user_key, "deviceType": device_type},
            timeout=2
        )

        if r.status_code == 200 and (r.json() or {}).get("statusCode") == 200:
            return jsonify(statusCode=200, message="success"), 200

        return jsonify(statusCode=400, message="bad_request"), 400
    except Exception:
        return jsonify(statusCode=400, message="bad_request"), 400

@app.get("/Log/auth/statistics")
def statistics():
    device_type = request.args.get("deviceType", "")

    # spec: if failed then -> count -1
    if device_type not in ALLOWED:
        return jsonify(deviceType=device_type, count=-1), 200

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM device_registrations WHERE device_type=%s;", (device_type,))
        count = cur.fetchone()[0]
        cur.close()
        conn.close()

        return jsonify(deviceType=device_type, count=int(count)), 200
    except Exception:
        return jsonify(deviceType=device_type, count=-1), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)