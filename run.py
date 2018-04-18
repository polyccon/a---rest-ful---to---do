import os
import uuid

import sqlite3
from flask import Flask
from flask import jsonify, request, abort, make_response
from flask import redirect, flash, session
from flask_sqlalchemy import SQLAlchemy

import db_queries


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"


@app.before_request
def before_request():
    if not request.endpoint in ['login', 'logout']:
        try:
            key = request.headers['API_key']
        except KeyError:
            abort(400, 'No api key provided')
        if not db_queries.is_token(key)[0]:
            abort(401, 'Invalid API key')

@app.route('/')
def home():
    if not session.get('logged_in'):
        return make_response(jsonify({"message":'Unauthorised. Please login.'}), 401)

@app.route('/login', methods=['POST'])
def login():
    try:
        request_body = request.get_json()
        username = request_body['username']
        password = request_body['password']
        user_db = db_queries.get_user(username)
        if username == user_db[1] and password == user_db[2]:
            session['logged_in'] = True
            token = uuid.uuid4()
            db_queries.store_token(token, user_db[1])
            return make_response(jsonify({"token":str(token)}), 200)
        else:
            flash('wrong password!')
            return make_response(jsonify({"message":'Wrong password'}), 400)
    except Exception as e:
        print ('error', e)
        return make_response(jsonify({"message":'Something went wrong'}), 400)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return make_response(jsonify({"message":'You\'ve now logged out'}), 200)

@app.route("/<user>")
def get_todo(user):
    tasks = db_queries.get_todo(user)
    return make_response(jsonify({"tasks":tasks}), 200)


@app.route("/add", methods=['POST'])
def add():
    if not session.get('logged_in'):
        return home()
    else:
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
    if not session.get('logged_in'):
        return home()
    else:
        tasks = db_queries.delete_todo(task_id)
        return make_response(jsonify({"tasks":tasks}), 200)

@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    if not session.get('logged_in'):
        return home()
    else:
        tasks = db_queries.resolve_todo(task_id)
        return make_response(jsonify({"tasks":tasks}), 200)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='127.0.0.1', port=8000)
