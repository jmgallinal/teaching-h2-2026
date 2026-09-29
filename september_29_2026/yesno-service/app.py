import os
import random
import time

from flask import Flask, jsonify, request

app = Flask(__name__)

chaos = {
    "failure_rate": float(os.getenv("FAILURE_RATE", "0")),
    "latency_ms": int(os.getenv("LATENCY_MS", "0")),
}


def problem(status, title, detail, headers=None):
    resp = jsonify({"type": "about:blank", "title": title, "status": status,
                    "detail": detail, "instance": request.path})
    resp.status_code = status
    resp.headers["Content-Type"] = "application/problem+json"
    for k, v in (headers or {}).items():
        resp.headers[k] = v
    return resp


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api")
def answer():
    if chaos["latency_ms"] > 0:
        time.sleep(chaos["latency_ms"] / 1000)
    if random.random() < chaos["failure_rate"]:
        return problem(503, "Service Unavailable",
                       "Failure injected by chaos configuration.",
                       headers={"Retry-After": "1"})
    value = random.choice(["yes", "no"])
    return jsonify({"answer": value, "forced": False,
                    "image": f"https://yesno.wtf/assets/{value}/1.gif"})


@app.get("/admin/chaos")
def get_chaos():
    return jsonify(chaos)


@app.put("/admin/chaos")
def set_chaos():
    data = request.get_json(silent=True) or {}
    try:
        rate = float(data.get("failure_rate", chaos["failure_rate"]))
        latency = int(data.get("latency_ms", chaos["latency_ms"]))
    except (TypeError, ValueError):
        return problem(400, "Invalid parameters",
                       "'failure_rate' must be numeric and 'latency_ms' an integer.")
    if not 0 <= rate <= 1 or latency < 0:
        return problem(422, "Invalid parameters",
                       "'failure_rate' must be between 0 and 1 and 'latency_ms' >= 0.")
    chaos["failure_rate"], chaos["latency_ms"] = rate, latency
    return jsonify(chaos)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5002")))
