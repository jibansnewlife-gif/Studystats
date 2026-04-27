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

    # Daily data
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
    goal = 120
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

    # -----------------------------
    # INSIGHTS (v2.5)
    # -----------------------------
    insights = []

    if today_minutes == 0:
        insights.append("⚠️ You haven't studied today")

    if streak >= 3:
        insights.append(f"🔥 You're on a {streak}-day streak")

    if subject_totals:
        most = max(subject_totals, key=subject_totals.get)
        least = min(subject_totals, key=subject_totals.get)

        if subject_totals[most] > subject_totals[least] * 2:
            insights.append(f"📊 You focus a lot on {most}, consider more {least}")

    if today_minutes >= 180:
        insights.append("💪 Great effort today!")

    if total_sessions < 3:
        insights.append("🚀 Start building your study habit!")

    if not insights:
        insights.append("👍 You're doing well, keep going!")

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
        xp_next=xp_next,
        insights=insights
    )
    
    # -----------------------------
    # SMARTER INSIGHTS (v2.6)
    # -----------------------------

    # Weekly calculation
    today = datetime.now().date()

    last_7_days = [
        (today - timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(7)
    ]

    prev_7_days = [
        (today - timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(7, 14)
    ]

    # Minutes this week
    this_week_minutes = sum(
        e["duration"] for e in user_data if e["date"] in last_7_days
    )

    # Minutes last week
    prev_week_minutes = sum(
        e["duration"] for e in user_data if e["date"] in prev_7_days
    )

    # Weekly summary
    insights.append(f"📅 You studied {round(this_week_minutes/60,2)} hrs this week")

    # Consistency score
    days_studied = len(set(e["date"] for e in user_data if e["date"] in last_7_days))
    consistency = int((days_studied / 7) * 100)

    insights.append(f"📈 Consistency: {consistency}% this week")

    # Improvement detection
    if prev_week_minutes > 0:
        if this_week_minutes > prev_week_minutes:
            insights.append("🚀 You're improving compared to last week")
        elif this_week_minutes < prev_week_minutes:
            insights.append("⚠️ You're studying less than last week")
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

    duration = max(1, min(duration, 300))

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
        session["username"] = request.form["username"]
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