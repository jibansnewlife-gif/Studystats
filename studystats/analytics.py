import json
import os
from datetime import datetime, timedelta

DATA_FILE = "studystats_data.json"

def show_stats():
    if not os.path.exists(DATA_FILE):
        print("No study data found.")
        return

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    if not data:
        print("No study sessions logged yet.")
        return

    # Total stats
    total_minutes = sum(entry["duration"] for entry in data)
    total_hours = total_minutes / 60

    print(f"\nTotal study time: {total_hours:.2f} hours")
    print(f"Total sessions: {len(data)}")

    # Weekly stats
    today = datetime.now()
    week_ago = today - timedelta(days=7)

    weekly_minutes = 0

    for entry in data:
        entry_date = datetime.strptime(entry["date"], "%Y-%m-%d")
        if entry_date >= week_ago:
            weekly_minutes += entry["duration"]

    print(f"Study time this week: {weekly_minutes/60:.2f} hours")

    # Subject breakdown
    subject_totals = {}

    for entry in data:
        subject = entry["subject"]
        subject_totals[subject] = subject_totals.get(subject, 0) + entry["duration"]

    print("\nStudy time by subject:")
    for subject, minutes in subject_totals.items():
        print(f"- {subject}: {minutes/60:.2f} hours")