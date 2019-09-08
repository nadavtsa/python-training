from datetime import timedelta

from flask_restful import Api
from flask import Flask
from flask_jwt_extended import JWTManager
from user import UserRegister, UserResource, Users, UserLogin
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'nadav'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=180)
api = Api(app)

jwt = JWTManager(app)   # not creating the /auth endpoint


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(Users, '/users')
api.add_resource(UserLogin, '/login')

app.run(port=5000, debug=True)

