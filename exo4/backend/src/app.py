import os
import time
import psycopg
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]

def dsn():
    return f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}"

def wait_for_db(retries=30, delay=1):
    for _ in range(retries):
        try:
            with psycopg.connect(dsn()) as conn:
                return
        except Exception:
            time.sleep(delay)
    raise RuntimeError("Database not reachable")

def init_db():
    with psycopg.connect(dsn()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                );
            """)
        conn.commit()

@app.get("/api/health")
def health():
    return jsonify(status="ok", db_host=DB_HOST)

@app.get("/api/users")
def list_users():
    with psycopg.connect(dsn()) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, username, password FROM users ORDER BY id;")
            rows = cur.fetchall()
    return jsonify(users=[{"id": r[0], "username": r[1], "password": r[2]} for r in rows])

@app.post("/api/users")
def create_user():
    data = request.get_json(force=True, silent=True) or {}
    username = data.get("username")
    password = data.get("password")
    if username is None or password is None:
        return jsonify(error="username and password are required"), 400

    with psycopg.connect(dsn()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id;",
                (username, password),
            )
            new_id = cur.fetchone()[0]
        conn.commit()

    return jsonify(user={"id": new_id, "username": username, "password": password}), 201

@app.put("/api/users/<int:user_id>")
def update_user(user_id):
    data = request.get_json(force=True, silent=True) or {}
    password = data.get("password")
    if password is None:
        return jsonify(error="password is required"), 400

    with psycopg.connect(dsn()) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET password = %s WHERE id = %s;", (password, user_id))
            updated = cur.rowcount
        conn.commit()

    if updated == 0:
        return jsonify(error="not found"), 404
    return jsonify(message="updated", id=user_id)

@app.delete("/api/users/<int:user_id>")
def delete_user(user_id):
    with psycopg.connect(dsn()) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            deleted = cur.rowcount
        conn.commit()

    if deleted == 0:
        return jsonify(error="not found"), 404
    return jsonify(message="deleted", id=user_id)

if __name__ == "__main__":
    wait_for_db()
    init_db()
    port = int(os.environ.get("BACKEND_PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
