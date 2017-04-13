import os
import click
import connexion
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = connexion.App(__name__, specification_dir='../')
#app.add_api('swagger.yml')


#app = Flask(__name__)

app.app.config.update(dict(
        DATABASE=os.path.join('db', 'sqlite', 'ave.db')
))


def connect_db():
    """Connects to sqlite database with metadata"""
    print(app.app.config['DATABASE'])
    rv = sqlite3.connect(app.app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with app.app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def get_db():
    """Opens a new database connection if there is none yet for
    the current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.app.teardown_appcontext
def close_db(error):
    """Closes the database at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
