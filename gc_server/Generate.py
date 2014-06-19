#!/usr/bin/env python
# coding=utf-8
from xml.dom.minidom import Document
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from flask import g
import math
from xml.dom.minidom import Document

# configuration
DATABASE = 'gc_data.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


def generate_xml(items):#, tel, features, dishes):
    
    doc=Document()  #创建DOM文档对象
    InfoList = doc.createElement('infoList') #创建根元素
    doc.appendChild(InfoList)

    Title = doc.createElement('title')
    Title_text = doc.createTextNode('optimallist') #元素内容写入
    Title.appendChild(Title_text)
    InfoList.appendChild(Title)

    #items = (items,"none") ###################
    count = len(items)
    Count = doc.createElement('count')
    Count_text = doc.createTextNode(str(count))
    Count.appendChild(Count_text)
    InfoList.appendChild(Count)
    
    for it in items:
        if it == "none":
            break
        
        tel = get_tel(it[0])
        features = get_feature(it[0])
        dishes = get_dish(it[0])

        Item = doc.createElement('item')
        InfoList.appendChild(Item)
        #doc.appendChild(Item)

        ID = doc.createElement('id')
        ID_text = doc.createTextNode(it[0])
        ID.appendChild(ID_text)
        Item.appendChild(ID)
        
        Name = doc.createElement('name')
        Name_text = doc.createTextNode(it[1])
        Name.appendChild(Name_text)
        Item.appendChild(Name)
        
        Consume = doc.createElement('consume')
        Consume_text = doc.createTextNode(str(it[4]))
        Consume.appendChild(Consume_text)
        Item.appendChild(Consume)
        
        Rate = doc.createElement('rate')
        Rate_text = doc.createTextNode(str(it[5]))
        Rate.appendChild(Rate_text)
        Item.appendChild(Rate)
        
        Taste = doc.createElement('taste')
        Taste_text = doc.createTextNode(str(it[6]))
        Taste.appendChild(Taste_text)
        Item.appendChild(Taste)
        
        Env = doc.createElement('env')
        Env_text = doc.createTextNode(str(it[7]))
        Env.appendChild(Env_text)
        Item.appendChild(Env)
        
        Serv = doc.createElement('serv')
        Serv_text = doc.createTextNode(str(it[8]))
        Serv.appendChild(Serv_text)
        Item.appendChild(Serv)
        
        Lat = doc.createElement('lat')
        Lat_text = doc.createTextNode(str(it[16]))
        Lat.appendChild(Lat_text)
        Item.appendChild(Lat)
        
        Lng = doc.createElement('lng')
        Lng_text = doc.createTextNode(str(it[17]))
        Lng.appendChild(Lng_text)
        Item.appendChild(Lng)
        
        Address = doc.createElement('address')
        Address_text = doc.createTextNode(it[10])
        Address.appendChild(Address_text)
        Item.appendChild(Address)
        
        ItemClass = doc.createElement('itemclass')
        ItemClass_text = doc.createTextNode(it[3])
        ItemClass.appendChild(ItemClass_text)
        Item.appendChild(ItemClass)
        
        Tel = doc.createElement('tel')
        Tel_text = doc.createTextNode(tel[1])
        #Tel_text = doc.createTextNode(it[20])
        Tel.appendChild(Tel_text)
        Item.appendChild(Tel)

        features = features+['none']
        for feature in features:
            if feature == 'none':
                break
            Feature = doc.createElement('feature')
            Feature_text = doc.createTextNode(feature[1])
            #Feature_text = doc.createTextNode(it[21])
            Feature.appendChild(Feature_text)
            Item.appendChild(Feature)

        dishes = dishes+['none']
        for dish in dishes:
            if dish == 'none':
                break
            Dish = doc.createElement('dish')
            Dish_text = doc.createTextNode(dish[1])
            #Dish_text = doc.createTextNode(it[22])
            Dish.appendChild(Dish_text)
            Item.appendChild(Dish)
    return doc.toprettyxml()


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


