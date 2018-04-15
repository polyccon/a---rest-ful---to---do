import sqlite3
from flask import Flask
from flask import jsonify, request, abort, make_response
from flask import redirect
from flask import flash, session
import os

import db_queries


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"


@app.route('/')
def home():
    if not session.get('logged_in'):
        return make_response(jsonify({"message":'You need to login'}), 403)
    else:
        return make_response(jsonify({"message":'Congrats, you\'re logged in'}), 200)


@app.route('/login', methods=['POST'])
def do_admin_login():
    try:
        request_body = request.get_json()
        username = request_body['username']
        password = request_body['password']
        user_db = db_queries.get_user(username)

        if username == user_db[1] and password == user_db[2]:
            session['logged_in'] = True
            home()
            return redirect('/{}'.format(username))
        else:
            flash('wrong password!')
            return home()
    except Exception as e:
        print ('error', e)
        return make_response(jsonify({"message":'Something went wrong'}), 400)


@app.route("/<user>")
def get_todo(user):
    tasks = db_queries.get_todo(user)
    return make_response(jsonify({"tasks":tasks}), 200)


@app.route("/add", methods=['POST'])
def add():
    try:
        request_body = request.get_json()
        user = request_body['user']
        task = request_body['task']
        complete = request_body['complete']
        tasks= db_queries.add_todo(user, task, complete)

        return make_response(jsonify({"tasks":tasks}), 200)
    except:
        response = 'Error'
        return response

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    tasks = db_queries.delete_todo(task_id)
    return make_response(jsonify({"tasks":tasks}), 200)

@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    tasks = db_queries.resolve_todo(task_id)
    return make_response(jsonify({"tasks":tasks}), 200)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='127.0.0.1', port=8000)
