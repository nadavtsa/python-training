from flask_restful import Resource, reqparse
import sqlite3
from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_identity


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")

    @jwt_required
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item, 200
        else:
            return {'messgae': 'No item with name {}'.format(name)}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        item = cursor.execute("SELECT * FROM items WHERE name=?", (name,)).fetchone()
        connection.close()
        if item:
             return {'item': {'name': item[0], 'price': item[1]}}
        return None

    def post(self, name):
        item = self.find_by_name(name)
        if item:
            return {'message': 'An item with name {} already exists'.format(name)}, 400
        data = Item.parser.parse_args()
        try:
            self.insert({'name': name, 'price': data['price']})
        except:
            return {'messgae': 'An error has occured'}, 500
        item = {'name': name, 'price': data['price']}
        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        cursor.execute("INSERT INTO items VALUES (?, ?)", (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        item = self.find_by_name(name)
        if item:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("DELETE FROM items WHERE name=?", (name,))
            connection.commit()
            connection.close()
            return {'message': 'Item {} was deleted successfully'.format(name)}, 200
        return {'message': 'Item does not exist'}, 404


    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        if item:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("UPDATE items SET price=? WHERE name=?", (data['price'], name))
            connection.commit()
            connection.close()
            return {'message': 'Item was updated',
                    'item': {'name': name, 'price': data['price']}}, 200
        item = {'name': name, 'price': data['price']}
        try:
            self.insert(item)
        except:
            return {'messgae': 'An error has occured inserting the item'}, 500
        return item, 200


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        _items = cursor.execute("SELECT * FROM items").fetchall()
        connection.close()
        if user_id:
            return {'items': [{'name': item[0], 'price': item[1]} for item in _items]}, 200
        return {'meaasge': 'Please log in to get the items list'}


