from flask import Flask, request, jsonify
import time

core = Flask("core_service")
account_balance = 0

@core.route("/coreAPI", methods=["POST"])
def core_api():
    global account_balance
    data = request.json
    action = data.get("action")
    amount = data.get("amount", 0)

    if action == "deposit":
        account_balance += amount
        return jsonify({"new_balance": account_balance}), 200

    elif action == "withdraw":
        time.sleep(5)  # Simulating slow response
        if amount <= account_balance:
            account_balance -= amount
            return jsonify({"message": "OK"}), 200
        return jsonify({"error": "Insufficient funds"}), 400

    return jsonify({"error": "Invalid action"}), 400

if __name__ == "__main__":
    core.run(host="0.0.0.0", port=5001)
