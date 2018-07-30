from flask import Flask, request , jsonify, Blueprint
import re
from __init__ import app
import datetime
import psycopg2
import jwt
import hashlib

from models import *

users = Blueprint('users', __name__)


def make_pswd_hash(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_pswd_hash(password, hash):
	if make_pswd_hash(password)==hash:
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

class Users:

	@users.route('/register', methods=['POST'])
	def register():
		try:
			fname = request.get_json()["fname"]
			lname = request.get_json()["lname"]
			email = request.get_json()["email"]
			username = request.get_json()["username"]
			password = request.get_json()["password"]
			con_password = request.get_json()["confirm password"]
			hash1 = make_pswd_hash(password)
			if len(fname) == 0 or len(lname) == 0 or len(email) == 0 or len(username) == 0 or len(password) == 0:
				return jsonify({'message':'please fill in all the entries'}), 406
			if password != con_password:
				return jsonify({'message':'password does not match'}), 406
			else:
				cur.execute("SELECT * FROM users WHERE username = '"+username+"'")
				if cur.fetchone() is None:
					if validate_password(password):
						if validate_emal(email):
							cur.execute("INSERT INTO users(fname,lname,username,email,password)VALUES(%s, %s, %s, %s, %s);",\
								(fname, lname, username, email, hash1))
						else:
							return jsonify({'message':'invalid email format!!'}), 403
					else:
						return jsonify({'message':'invalid password format!!'}), 403
				else:
					return jsonify({'message':'username exists'}), 409
				connection.commit()
				return jsonify({'message' : 'you are succesfully registered'}), 200
		except KeyError:
			return jsonify({'message':'ensure all entry fields are available'}), 406

	@users.route('/login', methods=['POST'])
	def login():
		username = request.get_json()["username"]
		password = request.get_json()["password"]
		if len(username) == 0 or len(password) == 0:
			return jsonify({'message':'please fill in all the entries'}), 406
		cur.execute("SELECT COUNT(1) FROM users WHERE username = '"+username+"'") #checks if username is in the database
		if cur.fetchone()[0]:
			cur.execute("SELECT * FROM users WHERE username = '"+username+"'")
			for row in cur.fetchall():
				if check_pswd_hash(password, row[5]):
					token = jwt.encode({'password' : password,'username': row[3], 'exp' : datetime.datetime.utcnow() + \
						datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
					return jsonify({'message' :{'token' : token.decode('UTF-8')}}), 200
				else:
					return jsonify({'message' : 'wrong password'}), 401
		else:
			return jsonify({'message' : 'Username does not exist'}), 401
		cur.close()

	@users.route ('/get_user',methods=['GET'])
	def get_user():
		data=jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		username=data['username']
		cur.execute("SELECT * FROM users WHERE username='"+username+"'")
		result=cur.fetchall()
		if result is not None:
			return jsonify (result), 200
		else:
			return jsonify({'message':'user does not exist in the database'}), 404
		connection.commit()

	@users.route ('/logout',methods=['GET'])
	def logout():
		return jsonify({'message':'you are successfully logged out!!'}), 200