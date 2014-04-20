#!/usr/bin/env python
# coding=utf-8

# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from flask import g
import math
from xml.dom.minidom import Document
from Generate import generate_xml
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

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


def getdistance(lat1, lng1, lat2, lng2):
    EARTH_RADIUS = 6378.137
    radlat1 = math.radians(lat1)
    radlat2 = math.radians(lat2)
    a = math.radians(lat1) - math.radians(lat2)
    b = math.radians(lng1) - math.radians(lng2)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2),2) + math.cos(radlat1)*math.cos(radlat2)*math.pow(math.sin(b/2),2)))
    s = s * EARTH_RADIUS
    return s


def find_the_nearest(lat0, lng0):
    cx = sqlite3.connect("gc_data.db")
    cu = cx.cursor()
    cu.execute("select * from shop")
    item = cu.fetchone() # lat = item[12], lng = item[13]
    min_dis = getdistance(lat0, lng0, item[12], item[13])
    min_item = item
    items = cu.fetchall()
    for it in items:
        lat = it[12]
        lng = it[13]
        dis = getdistance(lat0, lng0, lat, lng)
        if dis < min_dis:
            min_item = it
            min_dis = dis
    return min_item

def get_the_nearest_3(lat, lng):
    cx = sqlite3.connect("gc_data.db")
    cu = cx.cursor()
    cu.execute("select * from shop")
    items = cu.fetchall()
    sorted_items = sorted(items, cmp=lambda x,y:cmp(getdistance(lat, lng, x[12], x[13]), getdistance(lat, lng, y[12], y[13])))  ######sorted(L, cmp=lambda x,y:cmp(x[1],y[1]))
    return sorted_items[0:3]


def get_feature(url):
    cx = sqlite3.connect("gc_data.db")
    cu = cx.cursor()
    cu.execute("select * from features where url='"+url+"'")
    features = cu.fetchall()
    return features

def get_dish(url):
    cx = sqlite3.connect("gc_data.db")
    cu = cx.cursor()
    cu.execute("select * from great_dishes where url='"+url+"'")
    dishes = cu.fetchall()
    return dishes

def get_tel(url):
    cx = sqlite3.connect("gc_data.db")
    cu = cx.cursor()
    cu.execute("select * from tel where url='"+url+"'")
    tel = cu.fetchone()
    return tel


@app.route('/sort/',methods=['GET'])
def get_sorted():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    lat = float(lat)
    lng = float(lng)
    items = get_the_nearest_3(lat, lng) ##
    return str(items)
 
@app.route('/loc/',methods=['GET'])
def data_get():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    lat = float(lat)
    lng = float(lng)
    near_item = find_the_nearest(lat, lng)
    tel = get_tel(near_item[0])
    features = get_feature(near_item[0])
    dishes = get_dish(near_item[0])
    ret = 'Your location is:(%s,%s)' %(lat,lng)
    ret = ret + 'the nearest shop is' + near_item[0] + str(tel) + str(features) +str(dishes)
    xm = generate_xml(near_item, tel, features, dishes)
    return str(xm)

@app.route('/data/post/',methods=['POST'])
def data_post():
    token = request.form.get('token')
    ret = '%s**%s' %(token,'post')
    return send_ok_json(ret) 


if __name__ == '__main__':
    app.run(host='0.0.0.0')