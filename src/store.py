import uuid

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


class TodoStore:
    @classmethod
    def get(cls, user_id):
        return MemoryStore.get("todo:%s" % user_id) or []

    @classmethod
    def add_todo(cls, user_id, task):
        todos = TodoStore.get(cls, user_id)
        newtodos = todos.append({"id":str(len(todos)+1), "description":"%s"% task,
                                                            "complete": False })
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
