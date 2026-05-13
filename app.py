from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

USERS_FILE = "users.json"
RECORDS_FILE = "records.json"


# ----------------------------
# CREATE FILES IF NOT EXISTS
# ----------------------------

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)

if not os.path.exists(RECORDS_FILE):
    with open(RECORDS_FILE, "w") as f:
        json.dump([], f)


# ----------------------------
# LOAD DATA
# ----------------------------

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def load_records():
    with open(RECORDS_FILE, "r") as f:
        return json.load(f)


def save_records(records):
    with open(RECORDS_FILE, "w") as f:
        json.dump(records, f, indent=4)


# ----------------------------
# SIGNUP API
# ----------------------------

@app.route("/signup", methods=["POST"])
def signup():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    users = load_users()

    # CHECK EXISTING USER
    for user in users:
        if user["username"] == username:
            return jsonify({
                "message": "User already exists"
            }), 400

    users.append({
        "username": username,
        "password": password
    })

    save_users(users)

    return jsonify({
        "message": "Signup successful"
    })


# ----------------------------
# LOGIN API
# ----------------------------

@app.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    users = load_users()

    for user in users:

        if user["username"] == username and user["password"] == password:

            return jsonify({
                "message": "Login successful",
                "user": username
            })

    return jsonify({
        "message": "Invalid username or password"
    }), 401


# ----------------------------
# SAVE LEARNING RECORD
# ----------------------------

@app.route("/save_record", methods=["POST"])
def save_record():

    data = request.json

    records = load_records()

    records.append(data)

    save_records(records)

    return jsonify({
        "message": "Record saved successfully"
    })


# ----------------------------
# GET ALL RECORDS FOR ADMIN
# ----------------------------

@app.route("/admin_records", methods=["GET"])
def admin_records():

    admin_password = request.args.get("password")

    if admin_password != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    records = load_records()

    return jsonify(records)


# ----------------------------
# GET ALL USERS
# ----------------------------

@app.route("/users", methods=["GET"])
def get_users():

    admin_password = request.args.get("password")

    if admin_password != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    users = load_users()

    return jsonify(users)


# ----------------------------
# DELETE RECORD
# ----------------------------

@app.route("/delete_record/<int:index>", methods=["DELETE"])
def delete_record(index):

    admin_password = request.args.get("password")

    if admin_password != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    records = load_records()

    if index >= len(records):
        return jsonify({
            "message": "Record not found"
        }), 404

    deleted = records.pop(index)

    save_records(records)

    return jsonify({
        "message": "Record deleted",
        "deleted": deleted
    })


# ----------------------------
# UPDATE RECORD
# ----------------------------

@app.route("/update_record/<int:index>", methods=["PUT"])
def update_record(index):

    admin_password = request.args.get("password")

    if admin_password != "admin":
        return jsonify({
            "message": "Unauthorized"
        }), 403

    records = load_records()

    if index >= len(records):
        return jsonify({
            "message": "Record not found"
        }), 404

    new_data = request.json

    records[index] = new_data

    save_records(records)

    return jsonify({
        "message": "Record updated successfully"
    })


# ----------------------------
# HOME ROUTE
# ----------------------------

@app.route("/")
def home():

    return jsonify({
        "message": "Smart Learning App Backend Running"
    })


# ----------------------------
# RUN SERVER
# ----------------------------

if __name__ == "__main__":
    app.run(debug=True)
