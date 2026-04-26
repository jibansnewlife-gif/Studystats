from flask import Flask, render_template, request, redirect, session
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)
app.secret_key = "dev-secret-key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")


def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        if username:
            session["username"] = username
            return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")


@app.route("/")
def home():
    if "username" not in session:
        return redirect("/login")

    username = session["username"]
    all_data = load_data()
    user_data = all_data.get(username, [])
    user_data = [e for e in user_data if 1 <= e["duration"] <= 600]

    # TOTAL
    total_minutes = sum(e["duration"] for e in user_data)
    total_hours = round(total_minutes / 60, 2)
    total_sessions = len(user_data)

    # SUBJECTS
    subject_totals = {}
    for e in user_data:
        subject_totals[e["subject"]] = subject_totals.get(e["subject"], 0) + e["duration"] / 60
    subject_totals = dict(sorted(subject_totals.items(), key=lambda x: x[1], reverse=True))

    # GRAPH
    daily_data = defaultdict(int)
    for i in range(7):
        day = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        daily_data[day] = 0

    for e in user_data:
        if e["date"] in daily_data:
            daily_data[e["date"]] += e["duration"]

    dates = list(daily_data.keys())
    minutes = list(daily_data.values())

    # STREAK
    streak = 0
    d = datetime.now()
    dates_set = set(e["date"] for e in user_data)

    while d.strftime("%Y-%m-%d") in dates_set:
        streak += 1
        d -= timedelta(days=1)

    # DAILY GOAL
    today = datetime.now().strftime("%Y-%m-%d")
    today_minutes = sum(e["duration"] for e in user_data if e["date"] == today)

    goal = 120
    goal_percent = min(100, int((today_minutes / goal) * 100))

    # XP SYSTEM
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


@app.route("/add", methods=["POST"])
def add():
    if "username" not in session:
        return redirect("/login")

    username = session["username"]
    duration = int(request.form["duration"])
    subject = request.form["subject"].strip()

    if duration < 1 or duration > 600:
        return redirect("/")

    all_data = load_data()
    if username not in all_data:
        all_data[username] = []

    all_data[username].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "duration": duration,
        "subject": subject
    })

    save_data(all_data)
    return redirect("/")


# DELETE FEATURE
@app.route("/delete/<int:index>")
def delete(index):
    if "username" not in session:
        return redirect("/login")

    username = session["username"]
    data = load_data()

    if username in data and 0 <= index < len(data[username]):
        data[username].pop(index)
        save_data(data)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)