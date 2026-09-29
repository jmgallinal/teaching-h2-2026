import os
import random
from datetime import date

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)
app.json.sort_keys = False
app.json.ensure_ascii = False

USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "http://localhost:5000")
YESNO_URL = os.getenv("YESNO_URL", "http://localhost:5002/api")


def problem(status, title, detail, headers=None):
    resp = jsonify({"type": "about:blank", "title": title, "status": status,
                    "detail": detail, "instance": request.path})
    resp.status_code = status
    resp.headers["Content-Type"] = "application/problem+json"
    for k, v in (headers or {}).items():
        resp.headers[k] = v
    return resp


def get_likes_distributed_systems():
    # TODO: implement
    raise NotImplementedError("get_likes_distributed_systems is not implemented")


@app.get("/random-user")
def random_user():
    return jsonify(get_likes_distributed_systems())


# TODO: implement GET /age?year_of_birth=<year>


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.errorhandler(NotImplementedError)
def not_implemented(err):
    return problem(501, "Not Implemented", str(err))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5001")),
            debug=os.getenv("FLASK_DEBUG") == "1")
