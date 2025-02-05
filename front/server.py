from flask import Flask, request, jsonify
import requests

front = Flask("front_service")
CORE_URL = "http://core:5001/coreAPI"

@front.route("/deposit", methods=["POST"])
def deposit():
    amount = request.json.get("amount", 0)
    response = requests.post(CORE_URL, json={"action": "deposit", "amount": amount})
    return jsonify(response.json()), response.status_code

@front.route("/withdraw", methods=["POST"])
def withdraw():
    amount = request.json.get("amount", 0)
    response = requests.post(CORE_URL, json={"action": "withdraw", "amount": amount})
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    front.run(host="0.0.0.0", port=5000)
