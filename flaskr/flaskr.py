#!/usr/bin/env python
# coding=utf-8

# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort,
render_template, flash

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

