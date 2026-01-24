import os
from flask import Flask,request,jsonify
import psycopg2

app = Flask(__name__)

DATABASE_URL= os.getenv("DATABASE_URL")
DEVICES = {"iOS", "Android", "Watch", "TV"}

def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS device_registrations (
            user_key TEXT NOT NULL,
            device_type TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            PRIMARY KEY (user_key, device_type)
        );
    """)

    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_device_type
        ON device_registrations(device_type);
    """)

    conn.commit()
    cur.close()
    conn.close()




@app.get("/healthz")
def healthz():
    return "ok"; 200

@app.post("/Device/Register")
def register_device():
    try:
        data = request.get_json(silent=True) or {}
        user_key = (data.get("userKey") or "").strip()
        device_type = data.get("deviceType") or ""

        if user_key == "" or device_type not in DEVICES:
            return jsonify(statusCode=400),400

        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(""" INSERT INTO device_registrations (user_key, device_type) VALUES (%s, %s) ON CONFLICT (user_key, device_type) DO NOTHING; """,
        (user_key, device_type))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify(statusCode=200), 200

    except Exception:
        return jsonify(statusCode=400), 400

print(app.url_map)

if __name__ == "__main__":
     init_db()
     app.run(host="0.0.0.0", port=8080)