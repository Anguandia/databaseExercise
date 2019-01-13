import os
from app import create_app
from flask import request, jsonify
from app.db import Db

config_name = os.getenv('FLASK_ENV')
app =create_app(config_name)

@app.route('/api/v1/humans', methods=['get'])
def deal():
    res = Db().get_humans()
    return jsonify({'msg': res})
    #elif request.method = 'post':
    #    return jsonify({'msg': db.create})

@app.route('/api/v1/humans', methods=['post'])
def new():
    data = request.json
    name = data['name']
    address = data['address']
    age = data['age']
    res = Db().create(name, address, age)
    return jsonify({'msg': res})
