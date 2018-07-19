from flask import *
from functools import wraps
import datetime

app = Flask(__name__)
user={}
diary_content={}

app.config['SECRET_KEY'] = 'brybzlee'

#home page route
@app.route ('/api/v1/',methods=['GET'])
def home():
    return jsonify({'message' : 'welcome to your diary'})

#registering a new user 
@app.route ('/api/v1/register',methods=['POST'])
def register():
    name =request.get_json()["name"]
    username =request.get_json()["username"]
    email =request.get_json()["email"]
    password =request.get_json()["password"]

    if username not in user:#checks if the username already exists
        user.update({username:{"name":name,"email":email,"password":password}})
        return jsonify(user)
    else:
            return jsonify({'message' : 'username already exist'})

def login_authorization(username, password):
    if username in user:
        if password == user[username]["password"]:
            return True
    return False

#a function to perfom deletion and insertion of an entry but still maintain the index position
def replace (old,new,lst):
    for each in lst:
        if each == old:
            index=lst.index(each)
            del lst[index]
            lst.insert(index,new)

#check if a user is in session
def logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return jsonify({'message' : 'please login to continue'})
        else:
            return f(*args, **kwargs)
    return wrap
#logging into the diary
@app.route ('/api/v1/login',methods=['POST'])
def login():
    username=request.get_json()["username"]
    password=request.get_json()["password"]
    if login_authorization(username, password):
        session['logged_in'] = True
        session['username'] = username
        return jsonify({'message' : 'welcome to your diary'}) 
    else:
        return jsonify({'message' : 'invalid credentials'})

#making an entry
@app.route ('/api/v1/make_entry',methods=['POST'])
@logged_in
def make_entry():
    username=session.get('username')
    entry=request.get_json()["entry"]
    if username not in diary_content:
        diary_content.update({username:[]})
    diary_content[username].append(entry)
    return jsonify({'message' : 'diary successfully updated'})

#displaying all entries
@app.route ('/api/v1/get_all',methods=['GET'])
@logged_in
def get_all():
    username=session.get('username')
    output={}
    for each in diary_content[username]:
        output.update({diary_content[username].index(each)+1:each})#displays all the entries by the user and updates a positional value by adding 1 to the index 
    return jsonify (output)

#displaying one entry
@app.route ('/api/v1/get_one/<int:entryID>',methods=['GET'])
@logged_in
def get_one(entryID):
    username=session.get('username')#get's username from session
    return jsonify({entryID:diary_content[username][entryID-1]})#displays the entry whose index in the list is less by 1 from the number entered as entryID

#updating an already existing entry into the diary
@app.route ('/api/v1/modify_entry/<int:entryID>',methods=['PUT'])
@logged_in
def modify_entry(entryID):
    entry=request.get_json()["entry"]
    username=session.get('username')
    old=diary_content[username][entryID-1]
    replace (old, entry,diary_content[username])#invokes the replace function
    return jsonify({'message' :'entry successfully modified'})

#deleting a single entry by a user
@app.route ('/api/v1/delete_entry/<int:entryID>',methods=['DELETE'])
@logged_in
def delete_entry(entryID):
    username=session.get('username')#get's username from the username stored in session
    del diary_content[username][entryID-1]#deletes the entry whose index in the list is less by 1 from the number entered as entryID
    return jsonify ({'message' : 'succesfully deleted'})

#ending a user session 
@app.route ('/api/v1/logout',methods=['GET'])
@logged_in
def logout():
    session.clear()
    return jsonify({'message' : 'you are successfully logged out'})


#script initialization
if __name__== '__main__':
    app.run(debug=True)