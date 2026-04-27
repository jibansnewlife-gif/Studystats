from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "dev-secret-key"

# -----------------------------
# DATABASE SETUP
# -----------------------------
def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        date TEXT,
        duration INTEGER,
        subject TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# -----------------------------
# HOME
# -----------------------------
@app.route("/")
def home():
    if "username" not in session:
        return redirect("/login")

    username = session["username"]

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""
        SELECT id, date, duration, subject
        FROM sessions
        WHERE username=?
        ORDER BY id DESC
    """, (username,))

    rows = c.fetchall()
    conn.close()

    user_data = [
        {"id": r[0], "date": r[1], "duration": r[2], "subject": r[3]}
        for r in rows
    ]

    # -----------------------------
    # STATS
    # -----------------------------
    total_minutes = sum(e["duration"] for e in user_data)
    total_hours = round(total_minutes / 60, 2)
    total_sessions = len(user_data)

    # Subject totals
    subject_totals = {}
    for e in user_data:
        subject_totals[e["subject"]] = subject_totals.get(e["subject"], 0) + e["duration"]

    subject_totals = {
        k: round(v / 60, 2) for k, v in subject_totals.items()
    }

    # Daily data for chart
    daily_data = {}
    for e in user_data:
        daily_data[e["date"]] = daily_data.get(e["date"], 0) + e["duration"]

    dates = list(daily_data.keys())[::-1]
    minutes = list(daily_data.values())[::-1]

    # -----------------------------
    # STREAK
    # -----------------------------
    streak = 0
    today = datetime.now().date()

    for i in range(100):
        day = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        if any(e["date"] == day for e in user_data):
            streak += 1
        else:
            break

    # -----------------------------
    # DAILY GOAL
    # -----------------------------
    goal = 120  # minutes
    today_str = today.strftime("%Y-%m-%d")

    today_minutes = sum(
        e["duration"] for e in user_data if e["date"] == today_str
    )

    goal_percent = min(int((today_minutes / goal) * 100), 100)

    # -----------------------------
    # XP SYSTEM
    # -----------------------------
    xp = total_minutes
    level = xp // 500 + 1
    xp_next = (level * 500) - xp

    return render_template(
        "index.html",
        username=username,
        data=user_data,
        total_hours=total_hours,
        total_sessions=total_sessions,
        subject_totals=subject_totals,
        dates=dates,
        minutes=minutes,
        streak=streak,
        today_minutes=today_minutes,
        goal=goal,
        goal_percent=goal_percent,
        xp=xp,
        level=level,
        xp_next=xp_next
    )

# -----------------------------
# ADD SESSION
# -----------------------------
@app.route("/add", methods=["POST"])
def add():
    if "username" not in session:
        return redirect("/login")

    username = session["username"]

    try:
        duration = int(request.form["duration"])
    except:
        return redirect("/")

    duration = max(1, min(duration, 300))  # 1–300 min

    subject = request.form["subject"]
    date = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO sessions (username, date, duration, subject)
        VALUES (?, ?, ?, ?)
    """, (username, date, duration, subject))

    conn.commit()
    conn.close()

    return redirect("/")

# -----------------------------
# DELETE SESSION
# -----------------------------
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("DELETE FROM sessions WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")

# -----------------------------
# LOGIN
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        session["username"] = username
        return redirect("/")

    return render_template("login.html")

# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)