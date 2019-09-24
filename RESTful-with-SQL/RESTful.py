from datetime import timedelta

from flask_restful import Api
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from user import UserRegister, UserResource, Users, UserLogin, TokenRefresh, UserLogout
from item import Item, ItemList
from blacklist import BLACKLIST

app = Flask(__name__)
app.secret_key = 'nadav'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=180)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
api = Api(app)

jwt = JWTManager(app)   # not creating the /auth endpoint


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({'description': 'The token has expired',
                    'error': 'token_expired'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'description': 'Signature verification failed',
                    'error': 'Invalid token'}), 401


@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({'description': 'Request does not contain access token',
                    'error': 'authorization required'}), 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return jsonify({'description': 'The token is not fresh',
                    'error': 'Fresh token required'}), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({'description': 'The token has been revoked',
                    'error': 'token_revoked'}), 401

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(Users, '/users')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

app.run(port=5000, debug=True)

