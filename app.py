from flask import Flask, request, jsonify, render_template
import pymysql
import os
from datetime import datetime

app = Flask(__name__)

# MySQL Configuration
MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql-service')
MYSQL_USER = os.getenv('MYSQL_USER', 'taskuser')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'taskpass123')
MYSQL_DB = os.getenv('MYSQL_DB', 'tasks_db')

def get_db_connection():
    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status VARCHAR(50) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        tasks = cursor.fetchall()
        conn.close()
        return jsonify(tasks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tasks", methods=["POST"])
def add_task():
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description) VALUES (%s, %s)",
            (data.get("title"), data.get("description", ""))
        )
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        
        return jsonify({"id": task_id, "title": data.get("title")}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if "title" in data:
            cursor.execute("UPDATE tasks SET title = %s WHERE id = %s", (data["title"], task_id))
        if "description" in data:
            cursor.execute("UPDATE tasks SET description = %s WHERE id = %s", (data["description"], task_id))
        if "status" in data:
            cursor.execute("UPDATE tasks SET status = %s WHERE id = %s", (data["status"], task_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({"message": "Task updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        conn.close()
        
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tasks/<int:task_id>/status", methods=["PATCH"])
def toggle_task_status(task_id):
    try:
        data = request.get_json()
        status = data.get("status", "completed")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = %s WHERE id = %s", (status, task_id))
        conn.commit()
        conn.close()
        
        return jsonify({"message": "Task status updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    try:
        init_db()
    except Exception as e:
        print(f"Database initialization warning: {e}")
    
    app.run(host="0.0.0.0", port=5000, debug=False)
