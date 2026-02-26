from flask import Flask, render_template, request, redirect
from studystats.storage import log_session
import json
import os

app = Flask(__name__)

DATA_FILE = "studystats_data.json"

def get_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

@app.route("/")
def home():
    data = get_data()

    total_minutes = sum(entry["duration"] for entry in data)
    total_hours = total_minutes / 60

    subject_totals = {}
    for entry in data:
        subject = entry["subject"]
        subject_totals[subject] = subject_totals.get(subject, 0) + entry["duration"]

    return render_template(
        "index.html",
        total_hours=round(total_hours, 2),
        sessions=len(data),
        subject_totals=subject_totals,
        data=data
    )

@app.route("/log", methods=["POST"])
def log():
    duration = int(request.form["duration"])
    subject = request.form["subject"]
    log_session(duration, subject)
    return render_template("index.html",data=data,total_hours=total_hours,total_sessions=total_sessions)

if __name__ == "__main__":
    app.run()