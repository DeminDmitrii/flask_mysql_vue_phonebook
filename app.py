from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from db_service import Contacts

app = Flask(__name__, static_folder='frontend/dist/static', template_folder='frontend/dist')
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/contacts', methods=['GET'])
def get():
    return Contacts.get(request.args.get('term'))


@app.route('/api/contacts/', methods=['POST'])
def post():
    contact = request.json

    if len(contact['name']) == 0:
        return jsonify({'success': False, 'message': 'Поле `имя` обязательно'}), 200

    if len(contact['surname']) == 0:
        return jsonify({'success': False, 'message': 'Поле `фамилия` обязательно'}), 200

    if len(contact['phone']) == 0:
        return jsonify({'success': False, 'message': 'Поле `номер телефона` обязательно'}), 200

    return Contacts.post(contact)


@app.route('/api/contacts/', methods=['DELETE'])
def delete():
    return Contacts.delete(request.args.getlist('id'))


@app.route('/api/contacts/', methods=['PUT'])
def put():
    contact = request.json

    if len(contact['name']) == 0:
        return jsonify({'data': {'success': False, 'message': 'Поле `имя` обязательно'}})

    if len(contact['surname']) == 0:
        return jsonify({'data': {'success': False, 'message': 'Поле `фамилия` обязательно'}})

    if len(contact['phone']) == 0:
        return jsonify({'data': {'success': False, 'message': 'Поле `номер телефона` обязательно'}})

    return Contacts.put(contact)


if __name__ == '__main__':
    app.run()
