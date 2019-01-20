import os
from app import create_app
from flask import request, jsonify
from app.db import Db
from app import db_name

config_name = os.getenv('FLASK_ENV')
app =create_app(config_name)

@app.route('/api/v1/humans', methods=['get'])
def deal():
    res = Db(db_name).get_humans()
    return jsonify({'msg': res})
    #elif request.method = 'post':
    #    return jsonify({'msg': db.create})

@app.route('/api/v1/humans', methods=['post'])
def new():
    data = request.json
    name = data['name']
    address = data['address']
    age = data['age']
    res = Db(db_name).create(name, address, age)
    return jsonify({'msg': res})

@app.route('/api/v1/humans/<id>', methods=['delete'])
def delete(id):
    res = Db(db_name).delete_human(id)
    return jsonify({'msg': res})
