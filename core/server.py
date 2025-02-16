from flask import Flask, request, jsonify, Response
import time
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram

core = Flask("core_service")
account_balance = 0


REQUEST_COUNTER = Counter('core_requests_total', 'Total number of requests', ['method', 'endpoint', 'http_status'])
RESPONSE_TIME = Histogram('core_response_time_seconds', 'Response time in seconds', ['method', 'endpoint', 'action'])
WITHDRAW_PROCESSING_TIME = Histogram('core_withdraw_processing_time_seconds', 'Processing time for withdraw endpoint')

@core.before_request
def start_timer():
    request.start_time = time.time()
    if request.is_json:
        json_data = request.get_json(silent=True)
        request.action = json_data.get("action", "unknown") if json_data else "unknown"
    else:
        request.action = "unknown"

@core.after_request
def record_metrics(response):
    elapsed = time.time() - request.start_time
    # RESPONSE_TIME.labels(request.method, request.path).observe(elapsed)
    action = getattr(request, 'action', "unknown")
    RESPONSE_TIME.labels(method=request.method, endpoint=request.path, action=action).observe(elapsed)
    REQUEST_COUNTER.labels(request.method, request.path, response.status_code).inc()
    return response


@core.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


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
        with WITHDRAW_PROCESSING_TIME.time():
            time.sleep(5)  # Simulating slow response
            if amount <= account_balance:
                account_balance -= amount
                return jsonify({"message": "OK"}), 200
            return jsonify({"error": "Insufficient funds"}), 400

    return jsonify({"error": "Invalid action"}), 400

if __name__ == "__main__":
    core.run(host="0.0.0.0", port=5001)
