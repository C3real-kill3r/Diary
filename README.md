[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/e5f2eaa54ac38fce7214)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Build Status](https://travis-ci.org/C3real-kill3r/Diary.svg?branch=challenge3)](https://travis-ci.org/C3real-kill3r/Diary)
[![Coverage Status](https://coveralls.io/repos/github/C3real-kill3r/Diary/badge.svg?branch=challenge3)](https://coveralls.io/github/C3real-kill3r/Diary?branch=challenge3)
[![PyPI version](https://badge.fury.io/py/postman.svg)](https://badge.fury.io/py/postman)
[![PyPI version](https://badge.fury.io/py/sublime.svg)](https://badge.fury.io/py/sublime)

# Diary

it's an online journal where users can pen down their thoughts and feelings.
## Getting Started

download the zip folder into your computer.

### Prerequisites

* Postman
* Python (preferably version 3.6 or higher)
* Python IDE (preferably visual studio code or sublime)
* PostgresSQL
* Virtual environment

### Installing
* extract the files from the zip folder into another folder within the computer.

* open command prompt(in windows) or terminal (in Linux) and move to the folder directory containing the app.
* on the cmd; create virtual environment by typing:
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
* install flask in the virtual environment:
**for windows
```
(env)C:\>pip install flask
```
**for linux
```
$sudo pip3 install virtualenv
```
* pip install the requirements in your virtual environment
```
pip install -r requirements.txt
```
## Running the app

After successful installation of the app;

* open postgresSQl and create a database called "diary"

* create environment variables

```
set DB_NAME= enter your database name
set DB_USER= enter your database username
set DB_PASS= enter your database password
```

* run the ```run.py``` file in your virtual environment. 

* open postman

* press the ```Run in Postman``` button to populate your postman.

* if the variable environment doesn't get automatically configured in your post man;

1.type this on your login route under test;
```
var data = JSON.parse(responseBody);
postman.setEnvironmentVariable("token",data.message.token);
```
2. go to settings and select manage environment
3. add envronment, on key column write token but leave the value column empty


| Endpoint | **Functionality** | **Method** |
| ------ | ------ |------ |
| **api/v2/auth/signup** | Registers a new user |POST |
| **api/v2/auth/login** | logs in a registered user |POST |
| **api/v2/entries** | Fetch all entries |GET |
| **api/v2/entries/<entry_Id>** | Fetch a single entry |GET |
|**api/v2/entries**| Create an entry |POST |
| **api/v2/entries/<entry_Id>** | Modify an entry |PUT |
| **api/v2/entries/<entry_Id>** | Deletes an entry |DELETE |


## Built With

* [Sublime Text](http://www.sublimetext.com/) - The python text editor used
* [Postman](https://www.getpostman.com/) - For testing the end points

## Authors

* **Brian Ryb Okuku** 

