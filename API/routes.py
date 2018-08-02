from flask import jsonify, Blueprint

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
	return jsonify({'message':'welcome to your diary, your secure companion'})