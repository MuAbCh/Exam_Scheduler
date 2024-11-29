import json
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from scheduler_logic import optimize_schedule, loadexistingexams

app = Flask(__name__)

# Initialize schedules with existing exams
schedules = loadexistingexams()

# Path to your JSON file
JSON_FILE_PATH = "database/mock_data.json"

# Read data from the JSON file
def read_json_data():
    try:
        with open(JSON_FILE_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"courses": [], "students": [], "rooms": []}  # Return default structure if file is missing

# Write data to the JSON file
def write_json_data(data):
    with open(JSON_FILE_PATH, 'w') as f:
        json.dump(data, f, indent=4)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_schedule", methods=["GET"])
def get_schedule():
    calendar_events = []
    print(f"Current schedules: {schedules}")  # Debug log

    for schedule in schedules:
        try:
            date_str = schedule['date']       # Expected format: 'YYYY-MM-DD'
            time_str = schedule['time']       # Expected format: 'HH:MM'

            # Handle time format (ensure it's HH:MM)
            if len(time_str) == 5:
                time_format = '%H:%M'
            else:
                time_format = '%H:%M:%S'

            # Combine date and time into a datetime object
            start_datetime = datetime.strptime(f"{date_str} {time_str}", f'%Y-%m-%d {time_format}')
            exam_length = schedule.get('exam_length', 60)  # Default to 60 minutes if not provided
            end_datetime = start_datetime + timedelta(minutes=exam_length)

            event = {
                "title": f"{schedule['course']}{' - ' + schedule['room'] if schedule.get('room') else ''}",
                "start": start_datetime.isoformat(),
                "end": end_datetime.isoformat(),
                "allDay": False
            }
            print(f"Created event: {event}")  # Debug log
            calendar_events.append(event)
        except Exception as e:
            print(f"Error processing schedule: {schedule}. Exception: {e}")

    print(f"Returning events: {calendar_events}")  # Debug log
    return jsonify(calendar_events)

@app.route("/generate_schedule", methods=["POST"])
def generate_schedule():
    data = request.json
    print(f"Received POST data: {data}")  # Debug log

    # Ensure time is in HH:MM format
    time_str = data.get("preferred_time")
    if len(time_str) > 5:
        time_str = time_str[:5]

    new_schedule = {
        "course": data.get("course_name"),
        "room": data.get("room", ""),  # Set default to empty string if room is not provided
        "date": data.get("preferred_date"),
        "time": time_str,
        "exam_length": int(data.get("exam_length"))
    }

    # Update in-memory schedule
    schedules.append(new_schedule)
    print(f"Added new schedule: {new_schedule}")  # Debug log

    # Update the JSON file
    json_data = read_json_data()

    # Find the course by name
    course_name = new_schedule["course"]
    course_found = False
    for course in json_data["courses"]:
        if course["name"] == course_name:
            # Update the exam details for the found course
            course["exam"] = {
                "date": new_schedule["date"],
                "time": new_schedule["time"],
                "length": f"{new_schedule['exam_length']} minutes"  # Changed to minutes
            }
            course_found = True
            break

    if not course_found:
        # If the course is not found, add it
        json_data["courses"].append({
            "id": len(json_data["courses"]) + 1,  # Incremental ID
            "name": course_name,
            "students": [],  # Populate based on actual data if available
            "exam": {
                "date": new_schedule["date"],
                "time": new_schedule["time"],
                "length": f"{new_schedule['exam_length']} minutes"  # Changed to minutes
            }
        })

    # Write the updated JSON back to the file
    write_json_data(json_data)

    return jsonify([new_schedule])

@app.route("/optimize_schedule", methods=["POST"])
def optimize_schedule_route():
    global schedules
    mock_data = loadexistingexams()
    optimized_schedule = optimize_schedule(mock_data)
    schedules = optimized_schedule  # Update schedules with the optimized schedule
    return jsonify(optimized_schedule)

if __name__ == "__main__":
    app.run(debug=True)
