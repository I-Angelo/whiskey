from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Poison, poison_schema, poisons_schema

api = Blueprint('api', __name__, url_prefix = '/api')

# @api.route('/getdata')
# def getdata():
#     return {'yee': 'haw'}


@api.route('/poisons', methods = ['POST'])
@token_required
def create_poison(current_user_token):
    brand = request.json['brand'] 
    year = request.json['year']
    malt = request.json['malt']
    grain = request.json['grain']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    poison = Poison(brand, year, malt, grain, user_token = user_token) 

    db.session.add(poison) 
    db.session.commit() 

    response = poison_schema.dump(poison)
    return jsonify(response)

@api.route('/poisons', methods = ['GET'])
@token_required
def get_poison(current_user_token):
    a_user = current_user_token.token
    poisons = Poison.query.filter_by(user_token = a_user).all()
    response = poisons_schema.dump(poisons)
    return jsonify(response)    



@api.route('/poisons/<id>', methods = ['GET'])
@token_required
def get_single_poison(current_user_token, id):
    # a_user = current_user_token.token
    poison = Poison.query.get(id)
    response = poison_schema.dump(poison)
    return jsonify(response)


@api.route('/poisons/<id>', methods = ['POST', 'PUT'])
@token_required
def update_poison(current_user_token, id): 
    poison = Poison.query.get(id)
    poison.brand = request.json['brand']
    poison.year = request.json['year']
    poison.malt = request.json['malt']
    poison.grain = request.json['grain']
    poison.user_token = current_user_token.token

    db.session.commit()
    response = poison_schema.dump(poison)
    return jsonify(response)


@api.route('/poisons/<id>', methods = ['DELETE'])
@token_required
def delete_poison(current_user_token, id):
    # a_user = current_user_token.token
    poison = Poison.query.get(id)
    db.session.delete(poison)
    db.session.commit()
    response = poison_schema.dump(poison)
    return jsonify(response)