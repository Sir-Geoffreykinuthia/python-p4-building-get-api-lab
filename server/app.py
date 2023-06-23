#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def get_all_bakeries():
    all_bakeries = Bakery.query.all()
    bakeries_data = []
    for bakery in all_bakeries:
        bakery_data = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at,
            'updated_at': bakery.updated_at
        }
        bakeries_data.append(bakery_data)
    return jsonify(bakeries_data)

@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
        bakery_data = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at,
            'updated_at': bakery.updated_at,
            'baked_goods': []
        }
        for baked_good in bakery.baked_goods:
            baked_good_data = {
                'id': baked_good.id,
                'name': baked_good.name,
                'price': baked_good.price,
                'created_at': baked_good.created_at,
                'updated_at': baked_good.updated_at
            }
            bakery_data['baked_goods'].append(baked_good_data)
        return jsonify(bakery_data), 200
    else:
        return jsonify({'message': 'Bakery not found'}), 404

@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_data = []
    for baked_good in baked_goods:
        baked_good_data = {
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price,
            'created_at': baked_good.created_at,
            'updated_at': baked_good.updated_at
        }
        baked_goods_data.append(baked_good_data)
    return jsonify(baked_goods_data)

@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if baked_good:
        baked_good_data = {
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price,
            'created_at': baked_good.created_at,
            'updated_at': baked_good.updated_at
        }
        return jsonify(baked_good_data), 200
    else:
        return jsonify({'message': 'No baked goods found'}), 404
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)
