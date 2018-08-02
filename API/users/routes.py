from flask import Flask, request, jsonify, Blueprint
import re
from __init__ import app
import datetime
import psycopg2
from flask_restful import Api, Resource
import jwt
import hashlib

from models import *

users = Blueprint('users', __name__)
API = Api(users)


def make_pswd_hash(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_pswd_hash(password, hash):
	if make_pswd_hash(password) == hash:
		return True

	return False

def validate_emal(email):
	if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
		return False
	else:
		return True

def validate_password(password):
    if not re.match(r'^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])', password):
    	return False
    else:
    	return True

class Register(Resource):
	#@users.route('/auth/signup', methods=['POST'])
	def post(self):
		try:
			fname = request.get_json()["fname"].strip()
			lname = request.get_json()["lname"].strip()
			email = request.get_json()["email"].strip()
			username = request.get_json()["username"].strip()
			password = request.get_json()["password"].strip()
			con_password = request.get_json()["confirm password"].strip()
			hash1 = make_pswd_hash(password)
			if len(fname) == 0 or len(lname) == 0 or len(email) == 0 or len(username) == 0 or len(password) == 0:
				return jsonify({'message':'please fill in all the entries'})
			if password != con_password:
				return jsonify({'message':'password does not match'})
			else:
				cur.execute("SELECT * FROM users WHERE username = '"+username+"'")
				if cur.fetchone() is None:
					if validate_password(password):
						if validate_emal(email):
							cur.execute("INSERT INTO users(fname,lname,username,email,password)VALUES(%s, %s, %s, %s, %s);",\
								(fname, lname, username, email, hash1))
						else:
							return jsonify({'message':'invalid email format!!'})
					else:
						return jsonify({'message':'invalid format(must be 6 characters long with upper and lowercase letters, numbers and special characters) '}), 403
				else:
					return jsonify({'message':'username exists'})
				connection.commit()
				return jsonify({'message' : 'you are succesfully registered'})
		except KeyError:
			return jsonify({'message':'ensure all entry fields are available'})

class Login(Resource):
	#@users.route('/auth/login', methods=['POST'])
	def post(self):
		username = request.get_json()["username"].strip()
		password = request.get_json()["password"].strip()
		if len(username) == 0 or len(password) == 0:
			return jsonify({'message':'please fill in all the entries'})
		cur.execute("SELECT COUNT(1) FROM users WHERE username = '"+username+"'")
		if cur.fetchone()[0]:
			cur.execute("SELECT * FROM users WHERE username = '"+username+"'")
			for row in cur.fetchall():
				if check_pswd_hash(password, row[5]):
					token = jwt.encode({'password' : password,'username': row[3], 'exp' : datetime.datetime.utcnow() + \
						datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
					return jsonify({'message' :{'token' : token.decode('UTF-8')}})
				else:
					return jsonify({'message' : 'wrong password'})
		else:
			return jsonify({'message' : 'Username does not exist'})
		cur.close()

class User_details(Resource):
	#@users.route ('/get_user',methods=['GET'])
	def get(self):
		data=jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		username=data['username']
		cur.execute("SELECT * FROM users WHERE username='"+username+"'")
		result=cur.fetchone()
		user_id = result[0]
		fname = result[1]
		lname = result[2]
		username = result[3]
		email = result [4]
		password = result[5]
		time = result[6]
		user_details = {"user_id":user_id, "fname":fname, "lname":lname, "username":username, "email":email, "password":password, "time":time }
		if result is not None:
			return jsonify (user_details), 200
		else:
			return jsonify({'message':'user does not exist in the database'})
		connection.commit()

class Logout(Resource):
	#@users.route ('/logout',methods=['GET'])
	def get(self):
		return jsonify({'message':'you are successfully logged out!!'})

API.add_resource(Register, '/auth/signup')
API.add_resource(Login, '/auth/login')
API.add_resource(User_details, '/get_user')
API.add_resource(Logout, '/logout')