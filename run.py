import os
import json

import sqlite3
from flask import Flask
from flask import jsonify, request, abort, make_response
from flask import redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

import db_queries

SESSION_TYPE = 'redis'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config.from_object(__name__)

sess = Session()

@app.before_request
def before_request():
    username = session.get('username')
    print ('username', username)
    if request.endpoint in ['login', 'logout']:
        return
    if not username:
        abort(401, 'Login required.')
    if not db_queries.is_username_valid(username)[0]:
        abort(402, 'Invalid credentials, please login again.')


@app.route('/home')
def home():
    if not session.get('username'):
        return make_response(jsonify({"message":'Unauthorised. Please login.'}), 401)
    else:
        return

@app.route('/login', methods=['POST'])
def login():
    try:
        request_body = request.get_json()
        username = request_body['username']
        password = request_body['password']
        user_db = db_queries.get_user(username)
        db_username = user_db[1]
        db_password = user_db[2]
        if username == db_username and password == db_password:
            session['username'] = username
            return make_response(jsonify({"message":'You\'re now logged in'}), 200)

        else:
            flash('wrong password!')
            return make_response(jsonify({"message":'Wrong password'}), 400)
    except Exception as e:
        print ('error', e)
        return make_response(jsonify({"message":'Something went wrong'}), 400)

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


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
    except:
        return make_response(jsonify({"message":'Error'}), 400)
    try:
        tasks= db_queries.add_todo(user, task, complete)
        return make_response(jsonify({"tasks":tasks}), 200)
    except:
        return make_response(jsonify({"message":'Error'}), 500)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if not session.get('username'):
        return home()
    else:
        tasks = db_queries.delete_todo(task_id)
        return make_response(jsonify({"tasks":tasks}), 200)

@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    if not session.get('username'):
        return home()
    else:
        tasks = db_queries.resolve_todo(task_id)
        return make_response(jsonify({"tasks":tasks}), 200)


if __name__ == "__main__":
    app.secret_key = os.urandom(42)
    app.config['SESSION_TYPE'] = 'redis'
    sess.init_app(app)
    app.run(debug=True, host='127.0.0.1', port=8000)
