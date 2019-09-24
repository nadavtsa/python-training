import sqlite3
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_claims, jwt_refresh_token_required, get_jwt_identity,
    get_raw_jwt)


_user_parser = reqparse.RequestParser()

_user_parser.add_argument('username', type=str, required=True, help="Username field cannot be left blank!")
_user_parser.add_argument('password', type=str, required=True, help="Password field cannot be left blank!")

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username: str):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2])
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id: int):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

    def json(self):
        return {'id': self.id, 'username': self.username}



class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if User.find_by_username((data['username'])):
            return {'message': 'The username {} already exist'.format(data['username'])}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))
        connection.commit()
        connection.close()
        return {'message': 'username {} added successfully'.format(data['username'])}, 201


class UserResource(Resource):
    @classmethod
    def get(cls, user_id):
        user = User.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = User.find_by_id(user_id)
        if not user:
            return {'messgae': 'User not found'}, 404
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE username=?", (user.username,))
        connection.commit()
        connection.close()
        return {'message': 'User deleted successfully'}, 200


class Users(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        users = cursor.execute("SELECT * FROM users").fetchall()
        connection.close()
        return {'users': [{'id': user[0], 'username': user[1]} for user in users]}, 200

    @jwt_required
    def delete(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users")
        connection.commit()
        connection.close()
        return {'messgae': 'All users were deleted successfully'}


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = User.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out'}, 200

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        curr_user = get_jwt_identity()
        new_token = create_access_token(identity=curr_user, fresh=False)
        return {'access_token': new_token}, 200