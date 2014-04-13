#!/usr/bin/env python
# coding=utf-8
from xml.dom.minidom import Document

def generate_xml(items, tel, features, dishes):
    count = len(items)
    doc = Document()  #创建DOM文档对象
    InfoList = doc.createElement('InfoList') #创建根元素

    Title = doc.createElement('Title')
    Title_text = doc.createTextNode('OptimalList') #元素内容写入
    Title.appendChild(Title_text)
    InfoList.appendChild(Title)

    Count = doc.createElement('Count')
    Count_text = doc.createTextNode(str(count))
    Count.appendChild(Count_text)
    InfoList.appendChild(Count)
    items = (items,items)###################
    for it in items:
        Item = doc.createElement('Item')
        InfoList.appendChild(Item)

        ID = doc.createElement('ID')
        ID_text = doc.createTextNode(it[0])
        ID.appendChild(ID_text)
        Item.appendChild(ID)
        
        Name = doc.createElement('Name')
        Name_text = doc.createTextNode(it[1])
        Name.appendChild(Name_text)
        Item.appendChild(Name)
        
        Consume = doc.createElement('Consume')
        Consume_text = doc.createTextNode(str(it[7]))
        Consume.appendChild(Consume_text)
        Item.appendChild(Consume)
        
        Rate = doc.createElement('Rate')
        Rate_text = doc.createTextNode(str(it[3]))
        Rate.appendChild(Rate_text)
        Item.appendChild(Rate)
        
        Taste = doc.createElement('Taste')
        Taste_text = doc.createTextNode(str(it[4]))
        Taste.appendChild(Taste_text)
        Item.appendChild(Taste)
        
        Env = doc.createElement('Env')
        Env_text = doc.createTextNode(str(it[5]))
        Env.appendChild(Env_text)
        Item.appendChild(Env)
        
        Serv = doc.createElement('Serv')
        Serv_text = doc.createTextNode(str(it[6]))
        Serv.appendChild(Serv_text)
        Item.appendChild(Serv)
        
        Lat = doc.createElement('Lat')
        Lat_text = doc.createTextNode(str(it[12]))
        Lat.appendChild(Lat_text)
        Item.appendChild(Lat)
        
        Lng = doc.createElement('Lng')
        Lng_text = doc.createTextNode(str(it[13]))
        Lng.appendChild(Lng_text)
        Item.appendChild(Lng)
        
        Address = doc.createElement('Address')
        Address_text = doc.createTextNode(it[11])
        Address.appendChild(Address_text)
        Item.appendChild(Address)
        
        ItemClass = doc.createElement('ItemClass')
        ItemClass_text = doc.createTextNode(it[14])
        ItemClass.appendChild(ItemClass_text)
        Item.appendChild(ItemClass)
        
        Tel = doc.createElement('Tel')
        Tel_text = doc.createTextNode(str(tel))
        Tel.appendChild(Tel_text)
        Item.appendChild(Tel)

        features = features+['none','none','none']
        for i in range(0,3):
            Feature = doc.createElement('Feature')
            Feature_text = doc.createTextNode(str(features[i]))
            Feature.appendChild(Feature_text)
            Item.appendChild(Feature)

        dishes = dishes+['none','none']
        for i in range(0,2):
            Dish = doc.createElement('Dish')
            Dish_text = doc.createTextNode(str(dishes[i]))
            Dish.appendChild(Dish_text)
            Item.appendChild(Dish)
    return doc


