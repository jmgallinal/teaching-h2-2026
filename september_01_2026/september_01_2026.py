from flask import Flask, jsonify, request

app = Flask(__name__)

# Fake data, for now
users = [
    {'name': 'Josefina', 'email': 'jmgallinal@correo.um.edu.uy'},
    {'name': 'Daniel', 'email': 'dcanoniero@example.com'}
]

# Status codes
status_codes = {
    'OK': 200,
    'CREATED': 201,
    'BAD_REQUEST': 400,
    'NOT_FOUND': 404
}


@app.route('/', methods=['GET'])
def get():
    return jsonify('Welcome to Distributed Systems 2026. Atte: Jose')


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)


@app.route('/users/<string:user_email>', methods=['GET'])
def get_user(user_email):
    user = find_user_by_email(user_email)
    if user:
        return jsonify(user), status_codes['OK']
    else:
        return jsonify({'Error': 'User not found'}), status_codes['NOT_FOUND']


@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.json
    if not new_user or 'name' not in new_user or 'email' not in new_user:
        return jsonify({'Error': 'Bad Request'}), status_codes['BAD_REQUEST']

    user = {
        'name': new_user['name'],
        'email': new_user['email']
    }
    users.append(user)
    return jsonify(user), status_codes['CREATED']


# UTILS
def find_user_by_email(user_email):
    for user in users:
        if user['email'] == user_email:
            return user
    return None


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)


# USEFUL COMMANDS

### Run it without Docker
# pip install -r requirements.txt
# python september_01_2026.py

### Requests
# curl -X GET http://127.0.0.1:5000/
# curl -X GET http://127.0.0.1:5000/users
# curl -X GET http://127.0.0.1:5000/users/jmgallinal@correo.um.edu.uy

# Create a user
# curl -X POST http://127.0.0.1:5000/users \
#     -H "Content-Type: application/json" \
#     -d '{"name": "Josefina", "email": "jgallinal@example.com"}'

# Bad request (no email) -> should return 400, not 500
# curl -X POST http://127.0.0.1:5000/users \
#     -H "Content-Type: application/json" \
#     -d '{"name": "No Email"}'

### macOS note
# Port 5000 is used by AirPlay Receiver. If you run this without Docker and it
# says "address already in use", turn AirPlay Receiver off or change the port.
# With Docker this is not a problem: you map -p 5001:5000 and you are done.
