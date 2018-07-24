from flask import Flask, request , jsonify, Blueprint

main = Blueprint('main', __name__)

@main.route ('/api/v2/',methods=['GET'])
def home():
	return jsonify({'message':'welcome to your diary, your secure companion'}),200