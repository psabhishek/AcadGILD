import argparse
from time import gmtime, strftime

from flask import Flask, render_template, redirect, url_for, request,jsonify,send_from_directory
import shutil

import binascii
import os, sys, subprocess

import time
import requests
import json

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_ROOT = os.path.join(APP_ROOT,'static')



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    target = os.path.join(APP_ROOT, 'output/')
    if not os.path.isdir(target):
        os.mkdir(target)
    with open(os.path.join(target, 'txt.json')) as outfile:
        data = json.load(outfile)
    with open(os.path.join(target, 'txt2.json')) as logfile:
        logging = json.load(logfile)


    if request.method == 'POST':
        import pdb;pdb.set_trace()
        crc = str(request.form['Email'])
        if crc in data.keys() and data[crc][1]== request.form['password']:
            if crc in logging.keys():
                logging[crc]["Logins Count"] +=1
                logging[crc]["Time Stamp of last logins"].append(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                logging[crc]["current login timestamp"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            else:
                logging[crc] = {}
                logging[crc]["Logins Count"] = 1
                logging[crc]["Time Stamp of last logins"] = []
                logging[crc]["current login timestamp"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                logging[crc]["Time Stamp of last logins"].append(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            logging.update(logging)
            with open(os.path.join(target, 'txt2.json'), 'w') as f:
                json.dump(logging, f)
            return str(logging[crc])

        else:
            return "Email Or Password is wrong"



    return render_template('login.html', error=error)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    target = os.path.join(APP_ROOT, 'output/')
    if not os.path.isdir(target):
        os.mkdir(target)
    with open(os.path.join(target, 'txt.json')) as outfile:
        data = json.load(outfile)


    if request.method == 'POST':
        crc = str(request.form['Email'])
        if crc in data.keys():
            error = 'registered'
        else:
            data[crc] = (request.form['Phone Number'], request.form['password'],request.form['username'])
            data.update(data)
            with open(os.path.join(target, 'txt.json'), 'w') as f:
                json.dump(data, f)
                return "Please login at /login"
    return render_template('Signup.html', error=error)



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5123)
