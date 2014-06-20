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
import time
import datetime
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

def getoptscore(lat, lng, consume, sweet, sour, spicy, salty, order, time, x): #按照方差公式排序
    open_time = x[9]; #8~22  15位长001111111111111
    if time <= 8:
    	time = 8
    if time >=22:
    	time = 22
    istime = float(open_time[time-8])
    distance = getdistance(lat, lng, x[16], x[17])
    dconsume = (float(consume) - float(x[4]))
    dsweet = (float(sweet) - float(x[13]))
    dsour = (float(sour) - float(x[12]))
    dspicy = (float(spicy) - float(x[15]))
    dsalty = (float(salty) - float(x[14]))
    if istime == 1:
        score = distance*distance*10 + dconsume*dconsume + dsweet*dsweet + dsour*dsour + dspicy*dspicy +dsalty*dsalty
    else:
    	score = 99999999
    return score

def find_the_nearest(lat0, lng0):
    cx = sqlite3.connect("gc_data.db")
    cu = cx.cursor()
    cu.execute("select * from shop")
    item = cu.fetchone() # lat = item[12], lng = item[13]
    min_dis = getdistance(lat0, lng0, item[16], item[17])
    min_item = item
    items = cu.fetchall()
    for it in items:
        lat = it[16]
        lng = it[17]
        dis = getdistance(lat0, lng0, lat, lng)
        if dis < min_dis:
            min_item = it
            min_dis = dis
    return min_

def find_the_farest(lat0, lng0):
    cx = sqlite3.connect("gc_data.db")
    cu = cx.cursor()
    cu.execute("select * from shop")
    item = cu.fetchone() # lat = item[12], lng = item[13]
    max_dis = getdistance(lat0, lng0, item[16], item[17])
    max_item = item
    items = cu.fetchall()
    for it in items:
        lat = it[16]
        lng = it[17]
        dis = getdistance(lat0, lng0, lat, lng)
        if dis > max_dis:
            max_item = it
            max_dis = dis
    return max_item

def get_the_nearest(lat, lng, order):
    cx = sqlite3.connect("gc_data.db")
    cu = cx.cursor()
    t1 = time.time()
    cu.execute("select * from shop")
    items = cu.fetchall()
    t2 = time.time()
    sorted_items = sorted(items, cmp=lambda x,y:cmp(getdistance(lat, lng, x[16], x[17]), getdistance(lat, lng, y[16], y[17])))  ######sorted(L, cmp=lambda x,y:cmp(x[1],y[1]))
    t3 = time.time()
    print '数据库查询3205条数据花费：' + str((t2-t1)*1000) + '微秒，排序3205条数据花费：' + str((t3-t2)*1000) + '微秒'
    return sorted_items[0+int(order)*10:10+int(order)*10]

def get_the_optimal(lat, lng, consume, sweet, sour, spicy, salty, order, time):
    cx = sqlite3.connect("gc_data.db")
    cu = cx.cursor()
    cu.execute("select * from shop")
    items = cu.fetchall()
    sorted_items = sorted(items, cmp=lambda x,y:cmp(getoptscore(lat, lng, consume, sweet, sour, spicy, salty, order, time, x), getoptscore(lat, lng, consume, sweet, sour, spicy, salty, order, time, y)))  ######sorted(L, cmp=lambda x,y:cmp(x[1],y[1]))
    return sorted_items[0+int(order)*10:10+int(order)*10]


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


@app.route('/opt/',methods=['GET'])
def get_sorted(): #综合（opt）排序最近的3个
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    how = request.args.get('how')
    lat = float(lat)
    lng = float(lng)
    consume = request.args.get('consume')
    sweet = request.args.get('sweet')
    sour = request.args.get('sour')
    spicy = request.args.get('spicy')
    salty = request.args.get('salty')
    order = request.args.get('order')
    time = request.args.get('time')
    items = get_the_optimal(lat, lng, consume, sweet, sour, spicy, salty, order, time)
    #xm = ''
    '''for item in items:
        tel = get_tel(item[0])
        features = get_feature(item[0])
        dishes = get_dish(item[0])
        item = item + tel[1] + features[1] +dishes[1]'''
        #ret = 'Your location is:(%s,%s)' %(lat,lng)
        #ret = ret + 'the nearest shop is' + near_item[0] + str(tel) + str(features) +str(dishes)
    xm = generate_xml(items)
    return str(xm)
 
@app.route('/loc/',methods=['GET'])
def data_get():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    lat = float(lat)
    lng = float(lng)
    order = request.args.get('order')
    items = get_the_nearest(lat, lng, order)
    xm = generate_xml(items)
    return str(xm)

@app.route('/data/post/',methods=['POST'])
def data_post():
    token = request.form.get('token')
    ret = '%s**%s' %(token,'post')
    return send_ok_json(ret) 


if __name__ == '__main__':
    app.run(host='0.0.0.0')