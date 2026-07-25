from flask import Flask, request, jsonify
from time import sleep

app = Flask(__name__)
password = "86t4RF"

@app.route("/login", methods=["POST"])
def login():
    pwd = request.get_json().get("password", "")

    for i in range(len(password)):
        if i >= len(pwd) or pwd[i] != password[i]:
            return jsonify({"ok": False})
        sleep(0.01)

    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
