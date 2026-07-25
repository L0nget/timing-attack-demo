from flask import Flask, request, jsonify
from hmac import compare_digest
from hashlib import sha256

app = Flask(__name__)
password = "86t4RF"
password_hash = sha256(password.encode()).hexdigest()

@app.route("/login", methods=["POST"])
def login():
    pwd = request.get_json().get("password", "")

    user_hash = sha256(pwd.encode()).hexdigest()
    result = compare_digest(user_hash, password_hash)

    return jsonify({"ok": result})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
