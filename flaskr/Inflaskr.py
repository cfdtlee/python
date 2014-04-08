#!/usr/bin/env python
# coding=utf-8

# create our little application :)
app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

if __name__ == '__main__':
    app.run()
