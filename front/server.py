from flask import Flask, request, jsonify, Response
import requests
import time
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram

front = Flask("front_service")
CORE_URL = "http://core:5001/coreAPI"

REQUEST_COUNTER = Counter('front_requests_total', 'Total number of requests', ['method', 'endpoint', 'http_status'])
RESPONSE_TIME = Histogram('front_response_time_seconds', 'Response time in seconds', ['method', 'endpoint'])

def start_timer():
    request.start_time = time.time()

def record_metrics(response):
    elapsed = time.time() - request.start_time
    RESPONSE_TIME.labels(request.method, request.path).observe(elapsed)
    REQUEST_COUNTER.labels(request.method, request.path, response.status_code).inc()
    return response

@front.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

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
