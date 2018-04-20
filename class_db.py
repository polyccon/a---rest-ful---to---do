import os

from flask import Flask
from flask import jsonify, request, abort, make_response

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

class MemoryStore:
  pass

class UserStore:
  @classmethod
  def create(cls, name, password):
    MemoryStore.set("user:%s" % name, {'name': name, 'password': password})

  @classmethod
  def login(cls, name, password):
    user = MemoryStore.get("user:%s" % name)
    if user:
      return user["password"] == password
    else:
      return False

class TodoStore:
    @classmethod
    def get(cls, user_id):
        return MemoryStore.get("todo:%s" % user_id) or []

    @classmethod
    def add_todo(cls, user_id, task):
        todos = TodoStore.get(cls, user_id)
        newtodos = todos.append({"id":str(len(todos)+1), "description":"%s"% task, "complete": False })
        MemoryStore.set("todo:%s": "%" % user_id, newtodos)

    @classmethod
    def complete_task(cls, username, task_id):
        todos = TodoStore.get(cls, user_id)
        for item in todos:
            if item["id"] == str(task_id):
                item["complete"] == True
                MemoryStore.set("todo:%s": "%" % user_id, todos)
                break

    @classmethod
    def delete_task(cls, username, task_id):
        todos = TodoStore.get(cls, user_id)
        for item in todos:
            if item["id"] == str(task_id):
                todos.remove(item)
                MemoryStore.set("todo:%s": "%" % user_id, todos)
                break

@app.route("/get")
def get_todo():
    user_id = 1
    tasks = TodoStore.get(user_id)
    return make_response(jsonify({"tasks":tasks}), 200)

@app.route("/add", method=['POST'])
def add_todo():
    try:
        request_body = request.get_json()
        task = request_body['task']
    except:
        return make_response(jsonify({"message":'Error'}), 400)
    try:
        TodoStore.add(username, task)
        return get_todo()
    except:
        return make_response(jsonify({"message":'Error'}), 500)

@app.route("/complete/<id>", method=['PUT'])
def complete_task(task_id):
    try:
        TodoStore.complete(username, task_id)
        return get_todo()
    except:
        return make_response(jsonify({"message":'Error'}), 500)


@app.route("/delete/<id>", method=['DELETE'])
def complete_task(task_id):
    try:
        TodoStore.delete(username, task_id)
        return get_todo()
    except:
        return make_response(jsonify({"message":'Error'}), 500)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='127.0.0.1', port=8000)
