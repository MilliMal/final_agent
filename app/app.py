from flask import Flask, jsonify, request

app = Flask(__name__)

@flask_app.route('/', methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello, World!'})


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0')