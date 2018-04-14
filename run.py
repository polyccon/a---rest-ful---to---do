import sqlite3
from flask import Flask, jsonify, request, abort, make_response


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"


@app.route("/")
def main():
    testuser = 'user18081971'
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    tasks = c.execute("""SELECT * FROM todo WHERE user ='%s'"""% testuser).fetchall()
    conn.commit()
    conn.close()
    return make_response(jsonify({"tasks":tasks}), 200)


@app.route("/add", methods=['POST'])
def add():
    try:
        request_body = request.get_json()
        user = request_body['user']
        task = request_body['task']
        complete = request_body['complete']

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("""INSERT INTO todo (user, task, complete) VALUES (?, ?, ?)""", (user, task, complete))
        tasks = c.execute("""SELECT task FROM todo WHERE user ='%s'"""% user).fetchall()

        conn.commit()
        conn.close()
        return make_response(jsonify({"tasks":tasks}), 200)
    except:
        response = 'Error'
        return response

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("""DELETE FROM todo WHERE id ='%s'"""% task_id)
    conn.commit()
    conn.close()
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8000)
