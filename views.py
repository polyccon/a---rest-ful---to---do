import os
import uuid
from flask import Flask
from flask import jsonify, request, make_response, session

app = Flask(__name__)

class MemoryStore:
    @classmethod
    def init(cls):
        cls.store = dict()

    @classmethod
    def set(cls, key, value):
        cls.store[key] = value

    @classmethod
    def get(cls, key):
        return cls.store.get(key)

MemoryStore.init()


class UserStore:
  @classmethod
  def create(cls, username, password):
      user_id = str(uuid.uuid4())
      MemoryStore.set("user:%s" % username, {'id': user_id, 'username': username, 'password': password})

  @classmethod
  def login(cls, username, password):
    user = MemoryStore.get("user:%s" % username)
    if user is not None and user["password"] == password:
      return user
    else:
      return None


class TodoStore:
    @classmethod
    def get(cls, user_id):
        return MemoryStore.get("todo:%s" % user_id) or []

    @classmethod
    def add_todo(cls, user_id, task):
        todos = TodoStore.get(cls, user_id)
        newtodos = todos.append({"id":str(len(todos)+1), "description":"%s"% task, "complete": False })
        MemoryStore.set("todo:%s"% user_id, "%s" % newtodos)

    @classmethod
    def complete_task(cls, username, task_id):
        todos = TodoStore.get(cls, user_id)
        for item in todos:
            if item["id"] == str(task_id):
                item["complete"] == True
                MemoryStore.set("todo:%s"% user_id, "%s"% todos)
                break

    @classmethod
    def delete_task(cls, username, task_id):
        todos = TodoStore.get(cls, user_id)
        for item in todos:
            if item["id"] == str(task_id):
                todos.remove(item)
                MemoryStore.set("todo:%s"% user_id, "%s"%  todos)
                break

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

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='127.0.0.1', port=8000)
