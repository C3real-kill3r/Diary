[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/e5f2eaa54ac38fce7214)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

# Diary

an online journal where users can pen down their thoughts and feelings.
## Getting Started

download the zip folder into your computer.

### Prerequisites

*Postman
*Python (preferably version 3.6 or higher)
*Python IDE (preferably visual studio code or sublime)
*Virtual environment

### Installing
*extract the files from the zip folder into another folder within the computer.

*open command prompt(in windows) or terminal (in Linux) and move to the folder directory containing the app.
*on the cmd; create virtual environment by typing:
**for windows
```
C:\>virtualenv env
```
activate the virtual en 
```
C:\>env\Scripts\activate
```

**for linux
```
$virtualenv env
```
activate virtual env
```
$source env/bin/activate
```
*install flask in the virtual environment:
**for windows
```
(env)C:\>pip install flask
```
**for linux
```
$sudo pip3 install virtualenv
```

## Running the app

After successful installation of the app;
**run the app by typing in the command prompt/terminal:
*windows
```
(env)C:\>python diary.py 
```
*linux
```
$sudo python3 diary.py
```
*open postman
*press the run in postman button to populate your postman.

*if the variable environment doesn't get automatically configured in your post man;
1.type this on your login route under test;
```
var data = JSON.parse(responseBody);
postman.setEnvironmentVariable("token",data.message.token);
```
2. go to settings and select manage environment
3. add envronment, on key column write token but leave the value column empty

*enter the home url in postman to get started
```
http://127.0.0.1:5000/api/v2/
```
*register a new user into the system
```
http://127.0.0.1:5000/api/v2/register
```
*login the registered user in the system
```
http://127.0.0.1:5000/api/v2/login
```
*type as many entries as you'd prefer in the diary
```
http://127.0.0.1:5000/api/v2/make_entry{{token}}
```
*view all entries you have posted
```
http://127.0.0.1:5000/api/v2/get_all{{token}}
```
*modify an entry by typing the entry number in place of entryID
```
http://127.0.0.1:5000/api/v2/modify_entry/<int:entryID>{{token}}
```
*delete an entry by typing the entry number in place of entryID
```
http://127.0.0.1:5000/api/v2/delete_entry/<int:entryID>{{token}}
```
*logout from the diary
```
http://127.0.0.1:5000/api/v2/logout
```


## Built With

* [Sublime Text](http://www.sublimetext.com/) - The python text editor used
* [Postman](https://www.getpostman.com/) - For testing the end points

## Authors

* **Brian Ryb Okuku** 

