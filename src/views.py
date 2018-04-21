from flask import jsonify, request, make_response, session

from .store import *
from .core import app

@app.before_request
def before_request():
    username = session.get('username')
    if request.endpoint in ['login', 'logout']:
        return
    if username is None:
        return make_response(jsonify({"message":'Login required', "error": True}), 401)
    user = UserStore.get_one(username)
    if user is None:
        return make_response(jsonify({"message":'Invalid credentials, please login again.',
                                "error": True}), 401)
    else:
        return

@app.route('/login', methods=['POST'])
def login():
    try:
        request_body = request.get_json()
        username = request_body['username']
        password = request_body['password']
    except Exception as e:
        print ('error', e)
        return make_response(jsonify({"message":"Bad request", "error": True}), 400)
    user = UserStore.login(username, password)
    if user is not None:
        session['username'] = user['username']
        return make_response(jsonify({"message":'You\'re now logged in'}), 200)
    else:
        return make_response(jsonify({"message":"Invalid username or password",
                                        "error": True}), 400)

@app.route("/logout")
def logout():
    session.pop('username', None)
    return make_response(jsonify({"message":'You\'re now logged out'}), 200)

@app.route("/get")
def get_todo():
    username = session.get('username')
    try:
        tasks = TodoStore.get_all_by_user(username)
        return make_response(jsonify({"tasks":tasks}), 200)
    except Exception as e:
        print ('error', e)
        return make_response(jsonify({"message":'User todo list not found',
                                "error": True}), 500)

@app.route("/add", methods=['POST'])
def add_todo():
    username = session.get('username')
    try:
        request_body = request.get_json()
        task = request_body['task']
    except Exception as e:
        print ('error', e)
        return make_response(jsonify({"message":"Task key missing from request body",
                                        "error": True}), 400)
    try:
        TodoStore.add(username, task)
        return get_todo()
    except Exception as e:
        print ('error', e)
        return make_response(jsonify({"message":"Internal server error",
                                        "error": True}), 500)

@app.route("/complete/<task_id>", methods=['PUT'])
def complete_task(task_id):
    username = session.get('username')
    try:
        TodoStore.complete(username, task_id)
        return get_todo()
    except Exception as e:
        print ('error', e)
        return make_response(jsonify({"message":"Internal server error",
                                        "error": True}), 500)


@app.route("/delete/<task_id>", methods=['DELETE'])
def delete_task(task_id):
    username = session.get('username')
    try:
        TodoStore.delete(username, task_id)
        return get_todo()
    except Exception as e:
        print ('error', e)
        return make_response(jsonify({"message":"Internal server error",
                                        "error": True}), 500)
