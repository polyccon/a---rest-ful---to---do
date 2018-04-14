import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        c = conn.cursor()
        c.execute(''' CREATE TABLE todo
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user VARCHAR(100),
                    task VARCHAR(300), complete INT);''')

        c.execute('''INSERT INTO todo
                    VALUES (1, 'user18081971',
                    'wash the dishes', 0);''')
        conn.commit()
    except Error as e:
        print(e)
    finally:
        conn.close()

if __name__ == '__main__':
    create_connection("todo.db")
