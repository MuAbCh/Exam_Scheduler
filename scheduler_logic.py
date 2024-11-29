import json
import boto3

def optimize_schedule():
    # Load mock data
    with open("database/mock_data.json", "r") as f:
        data = json.load(f)

    # Dummy optimization logic
    schedule = [
        {"course": "ECE300", "room": "Room A", "time": "9:00 AM"},
        {"course": "ECE400", "room": "Room B", "time": "11:00 AM"}
    ]

    return schedule
