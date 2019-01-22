#!/usr/bin/env python
# encoding: utf-8
'''
@author: lurenjia
@contact: 1499418300@qq.com
@file: flask_demo.py
@time: 2018/7/17 17:44
@desc:
'''

from flask import Flask, jsonify, g, request, Response
from flask_cors import CORS
from model import AreaImg, DBsession, DBsession2, Test1
import sys
reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)
app.app_context().push()


@app.before_request
def before_request():
    pass


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'#处理跨域
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.route('/hello')
def hello():
    return jsonify({'data': 'hello world!'})


@app.route('/imgList')
def imgList():
    rows = DBsession2.execute('select * from temp1_v')
    ids = []
    for row in rows:
        ids.append({'id': row[0], 'name': row[1]})
    return jsonify({'data': ids})


@app.route('/img/<id>')
def getImgById(id):
    img = DBsession2.query(Test1).filter(Test1.id==id).one().img
    return Response(img, mimetype="image/jpeg")


@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload():
    if request.method == 'POST':
        area_img = Test1()
        area_img.name = request.files['file'].filename
        area_img.img = request.files['file'].read()
        DBsession2.add(area_img)
        DBsession2.commit()
        # print request.files['file'].read()
    return jsonify({'data': 'hello world!'})


def runFlask(port):
    app.config['SECRET_KEY'] = '123456'#全局变量才会用到
    app.run(port=port)
    CORS(app, supports_credentials=True)


if '__main__' == __name__:
    runFlask(8888)

