from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Store schedules in memory (replace with database in production)
schedules = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate_schedule", methods=["GET", "POST"])
def generate_schedule():
    if request.method == "GET":
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
                end_datetime = start_datetime + timedelta(hours=1)

                event = {
                    "title": f"{schedule['course']} - {schedule['room']}",
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

    elif request.method == "POST":
        data = request.json
        print(f"Received POST data: {data}")  # Debug log

        # Ensure time is in HH:MM format
        time_str = data.get("preferred_time")
        if len(time_str) > 5:
            time_str = time_str[:5]

        new_schedule = {
            "course": data.get("course_name"),
            "room": data.get("room"),
            "date": data.get("preferred_date"),
            "time": time_str
        }
        schedules.append(new_schedule)
        print(f"Added new schedule: {new_schedule}")  # Debug log
        return jsonify([new_schedule])

if __name__ == "__main__":
    app.run(debug=True)
