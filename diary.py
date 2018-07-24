from functools import wraps
from flask import Flask, request, jsonify, session



app = Flask(__name__)
USER = {}
DIARY_CONTENT = {}

app.config['SECRET_KEY'] = 'brybzlee'

#home page route
@app.route('/api/v1/', methods=['GET'])
def home():
    return jsonify({'message' : 'welcome to your diary'}), 200

#registering a new user 
@app.route('/api/v1/register', methods=['POST'])
def register():
    name = request.get_json()["name"]
    username = request.get_json()["username"]
    email = request.get_json()["email"]
    password = request.get_json()["password"]

    if username not in USER:#checks if the username already exists
        USER.update({username:{"name":name, "email":email, "password":password}})
        return jsonify(USER), 200
    else:
            return jsonify({'message' : 'username already exist'}), 409

def login_authorization(username, password):
    if username in USER:
        if password == USER[username]["password"]:
            return True
    return False

#a function to perfom deletion and insertion of an entry but still maintain the index position
def replace(old, new, lst):
    for each in lst:
        if each == old:
            index = lst.index(each)
            del lst[index]
            lst.insert(index, new)

#check if a user is in session
def logged_in(x_function):
    @wraps(x_function)
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return jsonify({'message' : 'please login to continue'}), 401
        else:
            return x_function(*args, **kwargs)
    return wrap
#logging into the diary
@app.route('/api/v1/login', methods=['POST'])
def login():
    username = request.get_json()["username"]
    password = request.get_json()["password"]
    if login_authorization(username, password):
        session['logged_in'] = True
        session['username'] = username
        return jsonify({'message' : 'welcome to your diary'}), 200 
    else:
        return jsonify({'message' : 'invalid credentials'}), 401

#making an entry
@app.route('/api/v1/make_entry', methods=['POST'])
@logged_in
def make_entry():
    username = session.get('username')
    entry = request.get_json()["entry"]
    if username not in DIARY_CONTENT:
        DIARY_CONTENT.update({username:[]})
    DIARY_CONTENT[username].append(entry)
    return jsonify({'message' : 'diary successfully updated'}), 200

#displaying all entries
@app.route('/api/v1/get_all', methods=['GET'])
@logged_in
def get_all():
    username = session.get('username')
    output = {}
    for each in DIARY_CONTENT[username]:
        output.update({DIARY_CONTENT[username].index(each)+1:each})#displays all the entries by the user and updates a positional value by adding 1 to the index 
    return jsonify(output), 200

#displaying one entry
@app.route('/api/v1/get_one/<int:entry_id>', methods=['GET'])
@logged_in
def get_one(entry_id):
    username = session.get('username')#get's username from session
    return jsonify({entry_id:DIARY_CONTENT[username][entry_id-1]}), 200#displays the entry whose index in the list is less by 1 from the number entered as entry_id

#updating an already existing entry into the diary
@app.route('/api/v1/modify_entry/<int:entry_id>', methods=['PUT'])
@logged_in
def modify_entry(entry_id):
    entry = request.get_json()["entry"]
    username = session.get('username')
    old = DIARY_CONTENT[username][entry_id-1]
    replace(old, entry, DIARY_CONTENT[username])#invokes the replace function
    return jsonify({'message' :'entry successfully modified'}), 200

#deleting a single entry by a user
@app.route('/api/v1/delete_entry/<int:entry_id>', methods=['DELETE'])
@logged_in
def delete_entry(entry_id):
    username = session.get('username')#get's username from the username stored in session
    del DIARY_CONTENT[username][entry_id-1]#deletes the entry whose index in the list is less by 1 from the number entered as entry_id
    return jsonify({'message' : 'succesfully deleted'}), 200

#ending a user session 
@app.route('/api/v1/logout', methods=['GET'])
@logged_in
def logout():
    session.clear()
    return jsonify({'message' : 'you are successfully logged out'}), 200


#script initialization
if __name__ == '__main__':
    app.run(debug=True)