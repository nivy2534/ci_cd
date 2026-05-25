from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

tasks = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    task = {
        "id": len(tasks) + 1,
        "title": data.get("title")
    }
    tasks.append(task)
    return jsonify(task), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
