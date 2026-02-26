from flask import Flask, render_template, request, redirect, session
import json
import os
from datetime import datetime

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

    total_minutes = sum(entry["duration"] for entry in user_data)
    total_hours = round(total_minutes / 60, 2)
    total_sessions = len(user_data)

    subject_totals = {}
    for entry in user_data:
        subject = entry["subject"]
        subject_totals[subject] = subject_totals.get(subject, 0) + entry["duration"] / 60

    return render_template(
        "index.html",
        username=username,
        data=user_data,
        total_hours=total_hours,
        total_sessions=total_sessions,
        subject_totals=subject_totals
    )


@app.route("/add", methods=["POST"])
def add():
    if "username" not in session:
        return redirect("/login")

    username = session["username"]
    duration = int(request.form["duration"])
    subject = request.form["subject"].strip()

    if duration < 1 or duration > 1440:
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
    app.run()