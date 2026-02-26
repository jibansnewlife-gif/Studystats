import json
import os
from datetime import datetime

DATA_FILE = "studystats_data.json"

def log_session(duration, subject):
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "duration": duration,
        "subject": subject
    }

    data = []

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

    data.append(entry)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print("Session logged successfully.")