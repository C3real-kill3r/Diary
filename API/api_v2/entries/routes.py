from flask import Flask, request , jsonify, Blueprint
import psycopg2
from __init__ import app
from functools import wraps
import datetime
import jwt

from models import *

entries = Blueprint('entries', __name__)


def require_token(f):
    @wraps(f)
    def wrap(*k, **kk):
        token = request.args.get('token') 

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        return f(*k, **kk)

    return wrap

class Entries():

	@entries.route('/api/v2/make_entry', methods=['POST'])
	@require_token
	def make_entry():
		title = request.get_json()["title"]
		comment = request.get_json()["comment"]
		data = jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
		username = data['username']
		cur.execute("INSERT INTO entries(title,comment,username)VALUES(%s,%s,%s);",(title, comment,username))
		connection.commit()
		return jsonify({'message':'entry successfully posted!!'}),200

	@entries.route('/api/v2/view_all', methods=['GET'])
	@require_token
	def view_all():
		data=jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
		username=data['username']	
		cur.execute("SELECT * FROM entries WHERE username='"+username+"'")
		result=cur.fetchall()
		connection.commit()
		return jsonify(result),200

	@entries.route('/api/v2/view_one/<int:entryID>', methods=['GET'])
	def view_one(entryID):
		data = jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
		username = data['username']
		cur.execute("SELECT COUNT(1) FROM entries WHERE username='"+username+"' and entryID='"+str(entryID)+"'")
		if cur.fetchone()[0]:
			cur.execute("SELECT * FROM entries WHERE username='"+username+"' and entryID='"+str(entryID)+"'")
			result = cur.fetchall()
			return jsonify(result)
		else:
			return jsonify({'message':'wrong entry,the comment does not exist!!'}), 401
		connection.commit()

	@entries.route ('/api/v2/modify_entry/<int:entryID>',methods=['PUT'])
	def modify_entry(entryID):
		comment = request.get_json()["comment"]
		data = jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
		username = data['username']
		today = str(datetime.datetime.today()).split()
		cur.execute("SELECT * FROM entries WHERE username='"+username+"' and entryID='"+str(entryID)+"'")
		result = cur.fetchone()
		if result is not None:
			if str(result[4]).split()[0] == today[0]:
				cur.execute("UPDATE entries SET comment='"+comment+"' WHERE entryID='"+str(entryID)+"'")
			else:
				return jsonify({'message':'not success, the comment is overdue'}),403
		else:
			return jsonify({'message':'operation not successfull!!'}),403
		connection.commit()
		return jsonify({'message':'entry successfully modified!!'}),200

	@entries.route('/api/v2/delete_entry/<int:entryID>', methods=['DELETE'])
	def delete_entry(entryID):
		data = jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
		username = data['username']
		cur.execute("SELECT * FROM entries WHERE username='"+username+"' and entryID='"+str(entryID)+"'")
		result = cur.fetchone()
		if result is None:
			return jsonify({'message':'the operation is not allowed'}),403
		else:
			cur.execute("DELETE FROM entries WHERE username='"+username+"' and entryID='"+str(entryID)+"'")
		connection.commit()
		return jsonify({'message':'entry successfully deleted!!'}),200