import sqlite3
from flask import Flask, render_template, request



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"


@app.route("/")
def main():
    testuser = 'user18081971'
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    tasks = c.execute("""SELECT task FROM todo WHERE user ='%s'"""% testuser).fetchone()
    c.close()
    return tasks







if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8000)
