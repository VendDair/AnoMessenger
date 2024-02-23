from os import name
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import sqlite3




app = Flask(__name__)
#CORS(app, resources={r"*": {"origins": "*"}})
CORS(app)
#cors = CORS(app, resources={r"/send": {"origins": "*"}})

@app.route("/clear", methods=["POST"])
def clear():
    db = sqlite3.connect("messages.db")
    cursor = db.cursor()
    cursor.execute("DELETE FROM messages")
    db.commit()
    return "200"

@cross_origin()
@app.route("/check", methods=["POST"])
def check():
    messages, names = read_all()
    if len(names) == 0:
        return jsonify(code="0")
    elif len(names) > request.json["length"]: 
        return jsonify(message=messages, names=names, code="200")
    else:
        return jsonify(code="202")


@cross_origin()
@app.route("/init", methods=["POST"])
def init():
    messages, names = read_all()
    return jsonify(message=messages, names=names)

def read_all():
    db = sqlite3.connect("messages.db")
    cursor = db.cursor()
    cursor.execute("SELECT text FROM messages")
    messages = cursor.fetchall()
    cursor.execute("SELECT name from messages")
    names = cursor.fetchall()
    return messages, names
@cross_origin()
@app.route("/send", methods=["POST"])
def main():
    new_message(request.json["data"], request.json["name"])
    response = jsonify(message=request.json["data"], name=request.json["name"])
    return response

def new_message(text: str, name: str):
    db = sqlite3.connect("messages.db")
    cursor = db.cursor()

    cursor.execute("INSERT INTO messages (name, text) VALUES (?, ?)", (name, text,))
    db.commit()
    cursor.close()
    db.close()

if __name__ == "__main__":
    app.run(debug=True, port=1234)
