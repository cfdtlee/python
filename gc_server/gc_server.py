#!/usr/bin/env python
# coding=utf-8

# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from flask import g

# configuration
DATABASE = 'gc_data.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config.from_object(__name__)

#cx = sqlite3.connect("gc_data.db")
#cu = cx.cursor()
#cu.execute("select * from backup_shop")
#item = cu.fetchone()
#cu.fetchall()

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username
 
@app.route('/loc/',methods=['GET'])
def data_get():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    ret = 'Your location is:(%s,%s)' %(lat,lng)
    return ret

@app.route('/data/post/',methods=['POST'])
def data_post():
    token = request.form.get('token')
    ret = '%s**%s' %(token,'post')
    return send_ok_json(ret) 


if __name__ == '__main__':
    app.run(host='0.0.0.0')