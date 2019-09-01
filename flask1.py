from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
    'name': 'My Store',
    'items': [
        {
        'name': 'My Item',
        'price': 25.75}
        ]
    }
]



@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)



@app.route('/store/<string:name>', methods=['GET'])
def get_store(name: str):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'error': 'store not found!'})



@app.route('/store')
def get_all_stores():
    return jsonify({'stores': stores})




@app.route('/store/<string:name>/item', methods=['POST'])
def create_items_in_store(name: str):
    for store in stores:
        if store['name'] == name:
            request_store = request.get_json()
            new_item = {
                'name': request_store['name'],
                'price': request_store['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'error': 'store not found'})



@app.route('/store/<string:name>/item', methods=['GET'])
def get_items_in_store(name: str):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'error': 'store not found!'})

app.run(port=5000)