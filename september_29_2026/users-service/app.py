import os
import random
import threading
import time

from flask import Flask, jsonify, request

app = Flask(__name__)
app.json.sort_keys = False
app.json.ensure_ascii = False

chaos = {
    "failure_rate": float(os.getenv("FAILURE_RATE", "0")),
    "latency_ms": int(os.getenv("LATENCY_MS", "0")),
}

SEED = [
    {"name": "Josefina", "email": "jmgallinal@correo.um.edu.uy"},
    {"name": "Daniel", "email": "dcanoniero@example.com"},
    {"name": "Maria", "email": "maria.perez@example.com"},
    {"name": "Carlos", "email": "carlos.martinez@example.com"},
    {"name": "Ana", "email": "ana.gomez@example.com"},
    {"name": "Luis", "email": "luis.flores@example.com"},
    {"name": "Elena", "email": "elena.romero@example.com"},
    {"name": "Pablo", "email": "pablo.jimenez@example.com"},
    {"name": "Laura", "email": "laura.cano@example.com"},
    {"name": "Miguel", "email": "miguel.alvarez@example.com"},
    {"name": "Sofia", "email": "sofia.vasquez@example.com"},
    {"name": "Jorge", "email": "jorge.mora@example.com"},
    {"name": "Natalia", "email": "natalia.silva@example.com"},
    {"name": "Fernando", "email": "fernando.mendoza@example.com"},
    {"name": "Isabel", "email": "isabel.torres@example.com"},
    {"name": "Raul", "email": "raul.sandoval@example.com"},
    {"name": "Camila", "email": "camila.martin@example.com"},
    {"name": "Andres", "email": "andres.suarez@example.com"},
    {"name": "Valeria", "email": "valeria.castillo@example.com"},
    {"name": "Samuel", "email": "samuel.garcia@example.com"},
]

lock = threading.Lock()
users = {i + 1: {"id": i + 1, **u} for i, u in enumerate(SEED)}
next_id = len(users) + 1


def problem(status, title, detail, headers=None):
    resp = jsonify({
        "type": "about:blank",
        "title": title,
        "status": status,
        "detail": detail,
        "instance": request.path,
    })
    resp.status_code = status
    resp.headers["Content-Type"] = "application/problem+json"
    for k, v in (headers or {}).items():
        resp.headers[k] = v
    return resp


def validate_user_payload(data):
    if not isinstance(data, dict):
        return "The body must be a JSON object."
    for field in ("name", "email"):
        if field not in data:
            return f"Missing required field '{field}'."
        if not isinstance(data[field], str) or not data[field].strip():
            return f"Field '{field}' must be a non-empty string."
    if "@" not in data["email"]:
        return "Field 'email' is not a valid email address."
    return None


@app.before_request
def inject_chaos():
    if request.path.startswith("/admin") or request.path == "/health":
        return None
    if chaos["latency_ms"] > 0:
        time.sleep(chaos["latency_ms"] / 1000)
    if random.random() < chaos["failure_rate"]:
        return problem(503, "Service Unavailable",
                       "Failure injected by chaos configuration.",
                       headers={"Retry-After": "1"})
    return None


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/users")
def list_users():
    all_users = list(users.values())
    try:
        offset = int(request.args.get("offset", 0))
        limit = int(request.args.get("limit", len(all_users)))
    except ValueError:
        return problem(400, "Invalid parameters",
                       "'limit' and 'offset' must be integers.")
    if offset < 0 or limit < 0:
        return problem(400, "Invalid parameters",
                       "'limit' and 'offset' must not be negative.")
    return jsonify(all_users[offset:offset + limit])


@app.get("/users/<int:user_id>")
def get_user(user_id):
    user = users.get(user_id)
    if user is None:
        return problem(404, "Not Found", f"User {user_id} does not exist.")
    return jsonify(user)


@app.post("/users")
def create_user():
    global next_id
    data = request.get_json(silent=True)
    error = validate_user_payload(data)
    if error:
        return problem(422, "Invalid data", error)
    with lock:
        user = {"id": next_id, "name": data["name"].strip(),
                "email": data["email"].strip()}
        users[next_id] = user
        next_id += 1
    resp = jsonify(user)
    resp.status_code = 201
    resp.headers["Location"] = f"/users/{user['id']}"
    return resp


@app.put("/users/<int:user_id>")
def replace_user(user_id):
    data = request.get_json(silent=True)
    error = validate_user_payload(data)
    if error:
        return problem(422, "Invalid data", error)
    with lock:
        if user_id not in users:
            return problem(404, "Not Found", f"User {user_id} does not exist.")
        user = {"id": user_id, "name": data["name"].strip(),
                "email": data["email"].strip()}
        users[user_id] = user
    return jsonify(user)


@app.delete("/users/<int:user_id>")
def delete_user(user_id):
    with lock:
        if users.pop(user_id, None) is None:
            return problem(404, "Not Found", f"User {user_id} does not exist.")
    return "", 204


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
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
