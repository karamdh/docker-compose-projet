import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_PATH = os.environ.get("DB_PATH", "/data/app.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
            """
        )
        conn.commit()


@app.get("/api/health")
def health():
    return jsonify(status="ok", db=DB_PATH)


@app.post("/api/users")
def create_user():
    data = request.get_json(force=True, silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if username is None or password is None:
        return jsonify(error="username and password are required"), 400

    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
            conn.commit()
        return jsonify(message="created", user={"username": username, "password": password}), 201
    except sqlite3.IntegrityError:
        return jsonify(error="user already exists"), 409


@app.get("/api/users")
def list_users():
    with get_conn() as conn:
        rows = conn.execute("SELECT username, password FROM users ORDER BY username").fetchall()
    users = [{"username": r["username"], "password": r["password"]} for r in rows]
    return jsonify(users=users)


@app.get("/api/users/<username>")
def get_user(username):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT username, password FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    if not row:
        return jsonify(error="not found"), 404
    return jsonify(user={"username": row["username"], "password": row["password"]})


@app.put("/api/users/<username>")
def update_user(username):
    data = request.get_json(force=True, silent=True) or {}
    new_password = data.get("password")

    if new_password is None:
        return jsonify(error="password is required"), 400

    with get_conn() as conn:
        cur = conn.execute(
            "UPDATE users SET password = ? WHERE username = ?",
            (new_password, username),
        )
        conn.commit()

    if cur.rowcount == 0:
        return jsonify(error="not found"), 404

    return jsonify(message="updated", user={"username": username, "password": new_password})


@app.delete("/api/users/<username>")
def delete_user(username):
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()

    if cur.rowcount == 0:
        return jsonify(error="not found"), 404

    return jsonify(message="deleted", username=username)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
