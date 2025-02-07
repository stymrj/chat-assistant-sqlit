from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to connect to SQLite database
def connect_db():
    conn = sqlite3.connect("company.db")
    conn.row_factory = sqlite3.Row  # Return results as dictionaries
    return conn

# Home Route
@app.route("/", methods=["GET"])
def home():
    return "Chat Assistant is running!"

# Chat Route (Handles user queries)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400
    
    user_query = data["message"].lower()
    response = process_query(user_query)
    
    return jsonify({"response": response})

# Function to process queries and execute SQL
def process_query(query):
    conn = connect_db()
    cursor = conn.cursor()

    # Query 1: Show all employees in a department
    if "employees in the" in query and "department" in query:
        dept = query.split("employees in the ")[1].split(" department")[0].capitalize()
        cursor.execute("SELECT Name FROM Employees WHERE Department=?", (dept,))
        result = cursor.fetchall()
        response = [row["Name"] for row in result] if result else ["No employees found"]

    # Query 2: Who is the manager of a department?
    elif "who is the manager of the" in query and "department" in query:
        dept = query.split("who is the manager of the ")[1].split(" department")[0].capitalize()
        cursor.execute("SELECT Manager FROM Departments WHERE Name=?", (dept,))
        result = cursor.fetchone()
        response = result["Manager"] if result else "Department not found"

    # Query 3: List all employees hired after a certain date
    elif "hired after" in query:
        date = query.split("hired after ")[1]
        cursor.execute("SELECT Name FROM Employees WHERE Hire_Date > ?", (date,))
        result = cursor.fetchall()
        response = [row["Name"] for row in result] if result else ["No employees found"]

    # Query 4: What is the total salary expense for a department?
    elif "total salary expense for the" in query and "department" in query:
        dept = query.split("total salary expense for the ")[1].split(" department")[0].capitalize()
        cursor.execute("SELECT SUM(Salary) FROM Employees WHERE Department=?", (dept,))
        result = cursor.fetchone()
        response = result[0] if result and result[0] else "No data found"

    else:
        response = "Sorry, I didn't understand your question."

    conn.close()
    return response

if __name__ == "__main__":
    app.run(debug=True)
