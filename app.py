from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3
import os

app = Flask(__tosolo__)

DB_NAME = os.path.join(os.getcwd(), "confessions.db")

def get_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS confessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            emotion TEXT NOT NULL,
            time TEXT NOT NULL,
            love INTEGER DEFAULT 0,
            sad INTEGER DEFAULT 0,
            wow INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# Initialize DB ON START
init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        text = request.form.get("confession")
        emotion = request.form.get("emotion")

        if text and emotion:
            conn = get_db()
            conn.execute(
                "INSERT INTO confessions (text, emotion, time) VALUES (?, ?, ?)",
                (text, emotion, datetime.now().strftime("%H:%M"))
            )
            conn.commit()
            conn.close()

        return redirect(url_for("home"))

    conn = get_db()
    confessions = conn.execute(
        "SELECT * FROM confessions ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("index.html", confessions=confessions)

@app.route("/react/<int:cid>/<reaction>")
def react(cid, reaction):
    if reaction not in ("love", "sad", "wow"):
        return redirect(url_for("home"))

    conn = get_db()
    conn.execute(
        f"UPDATE confessions SET {reaction} = {reaction} + 1 WHERE id = ?",
        (cid,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("home"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
