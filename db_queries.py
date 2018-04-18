import sqlite3

def get_todo(user):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    tasks = c.execute("""SELECT * FROM todo WHERE user ='%s'"""% user).fetchall()
    conn.commit()
    conn.close()
    return tasks

def add_todo(user, task, complete):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("""INSERT INTO todo (user, task, complete) VALUES (?, ?, ?)""", (user, task, complete))
    tasks = c.execute("""SELECT task FROM todo WHERE user ='%s'"""% user).fetchall()

    conn.commit()
    conn.close()
    return tasks

def delete_todo(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("""DELETE FROM todo WHERE id ='%s'"""% task_id)
    tasks = c.execute("""SELECT task FROM todo WHERE user ='%s'"""% user).fetchall()
    conn.commit()
    conn.close()
    return tasks

def resolve_todo(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    complete = c.execute("""SELECT complete FROM todo WHERE id ='%s'"""% task_id).fetchone()

    if complete == 0:
        complete =1
    else:
        complete = 0
    c.execute("""UPDATE todo SET complete= %s WHERE id ='%s'"""% (complete, task_id))
    tasks = c.execute("""SELECT task FROM todo WHERE user ='%s'"""% user).fetchall()
    conn.commit()
    conn.close()
    return tasks

def get_user(username):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    user = c.execute("""SELECT * FROM users WHERE user ='%s'"""% username).fetchone()
    conn.commit()
    conn.close()
    return user

def store_token(token, username):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("""UPDATE users SET token='%s' WHERE user ='%s';"""% (token, username))
    conn.commit()
    conn.close()
    return True

def is_token(token):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    tok = c.execute("""SELECT COUNT(*) FROM users WHERE token = '%s';"""% token).fetchone()
    conn.commit()
    conn.close()
    return tok
