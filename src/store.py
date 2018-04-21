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
  def get_one(cls, username):
      return MemoryStore.get("user:%s" % username)

  @classmethod
  def login(cls, username, password):
    user = MemoryStore.get("user:%s" % username)
    if user is not None and user["password"] == password:
      return user
    else:
      return None

UserStore.create('user18081971','Aphex')
UserStore.create('Tom Cruise','Top Gun')
UserStore.create('Dustin Hoffman','Rainman')
UserStore.create('Homer Simpson','TV')

class TodoStore:
    @classmethod
    def get_all_by_user(cls, username):
        return MemoryStore.get("todo:%s" % username) or []

    @classmethod
    def add(cls, username, task):
        todos = TodoStore.get_all_by_user(username)
        keys = ['id', 'description', 'complete']
        values = [str(len(todos)+1), task, False]
        todos.append(dict(zip(keys, values)))
        MemoryStore.set("todo:%s"% username, todos)

    @classmethod
    def complete(cls, username, task_id):
        todos = TodoStore.get_all_by_user(username)
        for item in todos:
            if item["id"] == str(task_id):
                item["complete"] = True
                MemoryStore.set("todo:%s"% username, todos)
                break

    @classmethod
    def delete(cls, username, task_id):
        todos = TodoStore.get_all_by_user(username)
        for item in todos:
            if item["id"] == str(task_id):
                todos.remove(item)
                MemoryStore.set("todo:%s"% username, todos)
                break
