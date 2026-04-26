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

    # TOTAL STATS
    total_minutes = sum(entry["duration"] for entry in user_data)
    total_hours = round(total_minutes / 60, 2)
    total_sessions = len(user_data)

    # SUBJECT TOTALS (sorted)
    subject_totals = {}
    for entry in user_data:
        subject = entry["subject"]
        subject_totals[subject] = subject_totals.get(subject, 0) + entry["duration"] / 60

    subject_totals = dict(sorted(subject_totals.items(), key=lambda x: x[1], reverse=True))

    # WEEKLY GRAPH DATA
    daily_data = defaultdict(int)

    for i in range(7):
        day = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        daily_data[day] = 0

    for entry in user_data:
        if entry["date"] in daily_data:
            daily_data[entry["date"]] += entry["duration"]

    dates = list(daily_data.keys())
    minutes = list(daily_data.values())

    # STREAK SYSTEM
    streak = 0
    current_day = datetime.now()
    dates_studied = set(entry["date"] for entry in user_data)

    while current_day.strftime("%Y-%m-%d") in dates_studied:
        streak += 1
        current_day -= timedelta(days=1)

    return render_template(
        "index.html",
        username=username,
        data=user_data,
        total_hours=total_hours,
        total_sessions=total_sessions,
        subject_totals=subject_totals,
        dates=dates,
        minutes=minutes,
        streak=streak
    )


@app.route("/add", methods=["POST"])
def add():
    if "username" not in session:
        return redirect("/login")

    username = session["username"]
    duration = int(request.form["duration"])
    subject = request.form["subject"].strip()

    # FIXED LIMIT (prevents insane values)
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


if __name__ == "__main__":
    app.run(debug=True)