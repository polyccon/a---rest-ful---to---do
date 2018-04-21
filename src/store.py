import uuid
import copy

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
      MemoryStore.set("user:%s" % username, {'id': user_id, 'username': username,
                                                            'password': password})

  @classmethod
  def login(cls, username, password):
    user = MemoryStore.get("user:%s" % username)
    if user is not None and user["password"] == password:
      return user
    else:
      return None

UserStore.create('user18081971','Aphex')

class TodoStore:
    @classmethod
    def get(cls, user_id):
        return MemoryStore.get("todo:%s" % user_id) or []

    @classmethod
    def add(cls, user_id, task):
        todos = TodoStore.get(user_id)
        print ('todos', todos, type(todos))
        keys = ['id', 'description', 'complete']
        values = [str(len(todos)+1), task, False]
        todos.append(dict(zip(keys, values)))
        MemoryStore.set("todo:%s"% user_id, todos)

    @classmethod
    def complete(cls, user_id, task_id):
        todos = TodoStore.get(user_id)
        for item in todos:
            if item["id"] == str(task_id):
                item["complete"] == True
                MemoryStore.set("todo:%s"% user_id, todos)
                break

    @classmethod
    def delete(cls, user_id, task_id):
        todos = TodoStore.get(user_id)
        for item in todos:
            if item["id"] == str(task_id):
                todos.remove(item)
                MemoryStore.set("todo:%s"% user_id, todos)
                break
