from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Route for the homepage (serves the frontend)
@app.route("/")
def home():
    return render_template("index.html")  # Flask will look in the 'templates' folder

# Route to handle scheduling logic (connects with the frontend)
@app.route("/generate_schedule", methods=["POST"])
def generate_schedule():
    # Retrieve data sent by the frontend
    data = request.json
    course_name = data.get("course_name")
    preferred_time = data.get("preferred_time")
    room = data.get("room")

    # Dummy schedule generation (for demo purposes)
    schedule = [
        {"course": course_name, "room": room, "time": preferred_time}
    ]

    # Return the generated schedule as JSON
    return jsonify(schedule)

if __name__ == "__main__":
    app.run(debug=True)
