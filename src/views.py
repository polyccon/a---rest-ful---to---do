from flask import jsonify, request, make_response, session

from .store import *
from .core import app

@app.before_request
def before_request():
    user_id = session.get('user_id')
    user = MemoryStore.get("user:%s" % user_id)
    if request.endpoint in ['login', 'logout']:
        return
    if not user_id:
        return make_response(jsonify({"error":'Login required'}), 401)
    user = MemoryStore.get("user:%s" % user_id)
    if not user:
        return make_response(jsonify({"error":'Invalid credentials, please login again.'}), 402)

@app.route('/login', methods=['POST'])
def login():
    try:
        request_body = request.get_json()
        username = request_body['username']
        password = request_body['password']
    except Exception as e:
        print ('error', e)
        return make_response(jsonify({"message":'Error: Bad request'}), 400)
    user = UserStore.login(username, password)
    if user:
        session['user_id'] = user['id']
        return make_response(jsonify({"message":'You\'re now logged in'}), 200)
    else:
        return make_response(jsonify({"message":'Error: Invalid username or password'}), 400)

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return make_response(jsonify({"message":'You\'re now logged out'}), 200)

@app.route("/get")
def get_todo():
    user_id = session.get('user_id')
    if user_id is not None:
        tasks = TodoStore.get(user_id)
        return make_response(jsonify({"tasks":tasks}), 200)
    else:
        return make_response(jsonify({"error":'Please login'}), 401)

@app.route("/add", methods=['POST'])
def add_todo():
    try:
        request_body = request.get_json()
        task = request_body['task']
    except Exception as e:
        print ('error', e)
        return make_response(jsonify({"message":'Error'}), 400)
    try:
        TodoStore.add(username, task)
        return get_todo()
    except Exception as e:
        print ('error', e)
        return make_response(jsonify({"message":'Error'}), 500)

@app.route("/complete/<id>", methods=['PUT'])
def complete_task(task_id):
    try:
        TodoStore.complete(username, task_id)
        return get_todo()
    except Exception as e:
        print ('error', e)
        return make_response(jsonify({"message":'Error'}), 500)


@app.route("/delete/<id>", methods=['DELETE'])
def delete_task(task_id):
    try:
        TodoStore.delete(username, task_id)
        return get_todo()
    except Exception as e:
        print ('error', e)
        return make_response(jsonify({"message":'Error'}), 500)
