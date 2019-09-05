from datetime import timedelta

from flask_restful import Api
from flask import Flask
from flask_jwt import JWT
from flask_jwt_extended import JWTManager
from user import UserRegister, UserResource, Users
from security import authenticate, identity
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'nadav'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=180)
api = Api(app)

jwt = JWTManager(app, authenticate, identity) # adds the auth endpoint



api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(Users, '/users')

app.run(port=5000, debug=True)

