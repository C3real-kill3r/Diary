from flask import *
import jwt
from models import *
import psycopg2
import re
from hashutl import make_pswd_hash, check_pswd_hash
from functools import wraps
import datetime

app = Flask(__name__)
app.config['SECRET_KEY']="brylee"

@app.route ('/api/v2/',methods=['GET'])
def home():
	return jsonify({'message':'welcome to your diary, your secure companion'}),200

def validate_emal(email):
	if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
		return False
	else:
		return True

@app.route ('/api/v2/register',methods=['POST'])
def register():
	fname=request.get_json()["fname"]
	lname=request.get_json()["lname"]
	email=request.get_json()["email"]
	username=request.get_json()["username"]
	password=request.get_json()["password"]
	con_password=request.get_json()["confirm password"]
	hash1=make_pswd_hash(password)
	if password != con_password:
		return jsonify({'message':'password does not match'}),403
	else:
		cur.execute("SELECT * FROM users WHERE username = '"+username+"'")
		if cur.fetchone() is None:
			if validate_emal(email):
				cur.execute("INSERT INTO users(fname,lname,username,email,password)VALUES(%s, %s, %s, %s, %s);",(fname, lname, username, email, hash1))
			else:
				return jsonify({'message':'invalid email format!!'})
		else:
			return jsonify({'message':'username exists'}),409
		connection.commit()
		return jsonify({'message' : 'you are succesfully registered'})


@app.route ('/api/v2/login',methods=['POST'])
def login():
	username=request.get_json()["username"]
	password=request.get_json()["password"]
	cur.execute("SELECT COUNT(1) FROM users WHERE username = '"+username+"'") #checks if username is in the database
	if cur.fetchone()[0]:
		cur.execute("SELECT * FROM users WHERE username = '"+username+"'")
		for row in cur.fetchall():
			if check_pswd_hash(password, row[5]):
				token = jwt.encode({'password' : password,'username': row[3], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
				return jsonify({'message' :{'token' : token.decode('UTF-8')}}),200
			else:
				return jsonify({'message' : 'wrong password'}),401
	else:
		return jsonify({'message' : 'Username does not exist'}),401
	cur.close()

def require_token(f):
    @wraps(f)
    def wrap(*k, **kk):
        token = request.args.get('token') 

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(*k, **kk)

    return wrap

@app.route ('/api/v2/make_entry',methods=['POST'])
@require_token
def make_entry():
	title=request.get_json()["title"]
	comment=request.get_json()["comment"]
	data=jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
	username=data['username']
	cur.execute("INSERT INTO entries(title,comment,username)VALUES(%s,%s,%s);",(title, comment,username))
	connection.commit()
	return jsonify({'message':'entry successfully posted!!'}),200

@app.route ('/api/v2/view_all',methods=['GET'])
@require_token
def view_all():
	data=jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
	username=data['username']	
	cur.execute("SELECT * FROM entries WHERE username='"+username+"'")
	result=cur.fetchall()
	connection.commit()
	return jsonify(result),200

@app.route ('/api/v2/view_one/<int:entryID>',methods=['GET'])
def view_one(entryID):
	data=jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
	username=data['username']
	cur.execute("SELECT COUNT(1) FROM entries WHERE username='"+username+"' and entryID='"+str(entryID)+"'")
	if cur.fetchone()[0]:
		cur.execute("SELECT * FROM entries WHERE username='"+username+"' and entryID='"+str(entryID)+"'")
		result=cur.fetchall()
		return jsonify(result)
	else:
		return jsonify({'message':'wrong entry,the comment does not exist!!'}),401
	connection.commit()

@app.route ('/api/v2/modify_entry/<int:entryID>',methods=['PUT'])
def modify_entry(entryID):
	comment=request.get_json()["comment"]
	data=jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
	username=data['username']
	today=str(datetime.datetime.today()).split()
	cur.execute("SELECT * FROM entries WHERE username='"+username+"' and entryID='"+str(entryID)+"'")
	result=cur.fetchone()
	if result is not None:
		if str(result[4]).split()[0]==today[0]:
			cur.execute("UPDATE entries SET comment='"+comment+"'")
			return jsonify({'message':'entry successfully modified!!'}),200
		else:
			return jsonify({'message':'not success, the comment is overdue'}),403
	else:
		return jsonify({'message':'operation not successfull!!'}),403
	connection.commit()

@app.route ('/api/v2/delete_entry/<int:entryID>',methods=['DELETE'])
def delete_entry(entryID):
	data=jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
	username=data['username']
	cur.execute("SELECT * FROM entries WHERE username='"+username+"' and entryID='"+str(entryID)+"'")
	result=cur.fetchone()
	if result is None:
		return jsonify({'message':'the operation is not allowed'}),403
	else:
		cur.execute("DELETE FROM entries WHERE username='"+username+"' and entryID='"+str(entryID)+"'")
		return jsonify({'message':'entry successfully deleted!!'}),200
	connection.commit()

@app.route ('/api/v2/get_user',methods=['GET'])
def get_user():
	data=jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
	username=data['username']
	cur.execute("SELECT * FROM users WHERE username='"+username+"'")
	result=cur.fetchall()
	if result is not None:
		return jsonify (result),200
	else:
		return jsonify({'message':'user does not exist in the database'})
	connection.commit()

@app.route ('/api/v2/logout',methods=['GET'])
def logout():
	return jsonify({'message':'you are successfully logged out!!'}),200

if __name__ == '__main__':
	create_tables()
	app.run(debug=True)