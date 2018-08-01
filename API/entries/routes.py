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
        token = request.headers.get('x-access-token') 

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        return f(*k, **kk)

    return wrap

class Entries:

	@entries.route('/entries', methods=['POST'])
	@require_token
	def make_entry():
		title = request.get_json()["title"].strip() 
		comment = request.get_json()["comment"].strip()
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		username = data['username']
		cur.execute("INSERT INTO entries(title,comment,username)VALUES(%s, %s, %s);",(title, comment,username))
		connection.commit()
		return jsonify({'message':'entry successfully posted!!'}), 200

	@entries.route('/entries', methods=['GET'])
	@require_token
	def view_all():
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		username = data['username']	
		cur.execute("SELECT * FROM entries WHERE username='"+username+"'")
		result = cur.fetchall()
		entry_output = {}
		for row in result:
			entry_id = row[0]
			title = row[1]
			time = row[4]
			comment = row[3]
			if entry_id not in entry_output:
				entry_output.update({entry_id:{"username":username, "title":title, "comment":comment, "time":time}})
		if len (result) == 0:
			return jsonify ({'message':'you have no comments yet'}), 200
		else:
			connection.commit()
			return jsonify(entry_output),200

	@entries.route('/entries/<int:entryID>', methods=['GET'])
	def view_one(entryID):
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		username = data['username']
		cur.execute("SELECT COUNT(1) FROM entries WHERE username='"+username+"' and entryID='"+str(entryID)+"'")
		if cur.fetchone()[0]:
			cur.execute("SELECT * FROM entries WHERE username='"+username+"' and entryID='"+str(entryID)+"'")
			result = cur.fetchone()
			entry_id = result[0]
			title = result[1]
			time = result[4]
			comment = result[3]
			entry_output = {"entry_id":entry_id, "username":username, "title":title, "comment":comment, "time":time }
			return jsonify(entry_output)
		else:
			return jsonify({'message':'wrong entry,the comment does not exist!!'}), 404
		connection.commit()

	@entries.route ('/entries/<int:entryID>',methods=['PUT'])
	def modify_entry(entryID):
		comment = request.get_json()["comment"].strip()#validate length of comment
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		username = data['username']
		today = str(datetime.datetime.today()).split()
		cur.execute("SELECT * FROM entries WHERE username='"+username+"' and entryID='"+str(entryID)+"'")
		result = cur.fetchone()
		if result is not None:
			if str(result[4]).split()[0] == today[0]:
				cur.execute("UPDATE entries SET comment='"+comment+"' WHERE entryID='"+str(entryID)+"'")
			else:
				return jsonify({'message':'not successfull, the comment is overdue'}),403
		else:
			return jsonify({'message':'enrtry does not exist!!'}) ,404
		connection.commit()
		return jsonify({'message':'entry successfully modified!!'}), 200

	@entries.route('/entries/<int:entryID>', methods=['DELETE'])
	def delete_entry(entryID):
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		username = data['username']
		cur.execute("SELECT * FROM entries WHERE username='"+username+"' and entryID='"+str(entryID)+"'")
		result = cur.fetchone()
		if result is None:
			return jsonify({'message':'this comment does exist'}), 404
		else:
			cur.execute("DELETE FROM entries WHERE username='"+username+"' and entryID='"+str(entryID)+"'")
		connection.commit()
		return jsonify({'message':'entry successfully deleted!!'}), 200