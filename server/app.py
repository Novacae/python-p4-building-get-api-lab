#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy.orm import sessionmaker
from models import db, Bakery, BakedGood
from sqlalchemy import create_engine


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
engine = create_engine('sqlite:///app.db')
Session = sessionmaker(bind=engine)

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

def get_bakeries():
    bakeries = Session.query(Bakery).all()
    bakeries_json = [bakery.to_dict() for bakery in bakeries]
    return jsonify(bakeries_json)


# Route to get a single bakery by ID
@app.route('/bakeries/<int:id>', methods=['GET'])
def get_bakery(id):
    session = Session()
    bakery = session.query(Bakery).filter_by(id=id).first()
    if bakery is None:
        session.close()
        return jsonify({'error': 'Bakery not found'}), 404
    bakery_json = bakery.to_dict(nested=True, exclude=['baked_goods'])
    bakery_json['baked_goods'] = [baked_good.to_dict() for baked_good in bakery.baked_goods]
    session.close()
    return jsonify(bakery_json)

@app.route('/baked_goods/by_price', methods=['GET'])
def get_baked_goods_by_price():
    session = Session()
    baked_goods = session.query(BakedGood).order_by(BakedGood.price.desc()).all()
    baked_goods_json = [baked_good.to_dict() for baked_good in baked_goods]
    session.close()
    return jsonify(baked_goods_json)


@app.route('/baked_goods/most_expensive', methods=['GET'])
def get_most_expensive_baked_good():
    session = Session()
    baked_good = session.query(BakedGood).order_by(BakedGood.price.desc()).first()
    if baked_good is None:
        session.close()
        return jsonify({'error': 'No baked goods found'}), 404
    baked_good_json = baked_good.to_dict()
    session.close()
    return jsonify(baked_good_json)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
