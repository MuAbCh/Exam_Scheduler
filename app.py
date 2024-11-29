from flask import Flask, render_template, jsonify
import scheduler_logic

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate_schedule", methods=["GET"])
def generate_schedule():
    schedule = scheduler_logic.optimize_schedule()
    return jsonify(schedule)

if __name__ == "__main__":
    app.run(debug=True)