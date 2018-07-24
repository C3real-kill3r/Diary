[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/337dee8ee33f349ab94d)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![PyPI version](https://badge.fury.io/py/postman.svg)](https://badge.fury.io/py/postman)
[![PyPI version](https://badge.fury.io/py/sublime.svg)](https://badge.fury.io/py/sublime)
[![Maintainability](https://api.codeclimate.com/v1/badges/622cfadf6b42f5843d83/maintainability)](https://codeclimate.com/github/C3real-kill3r/Diary/maintainability)
[![Build Status](https://travis-ci.org/C3real-kill3r/Diary.svg?branch=challenge2)](https://travis-ci.org/C3real-kill3r/Diary)
[![Test Coverage](https://api.codeclimate.com/v1/badges/622cfadf6b42f5843d83/test_coverage)](https://codeclimate.com/github/C3real-kill3r/Diary/test_coverage)

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
*enter the home url in postman to get started
```
http://127.0.0.1:5000/api/v1/
```
*register a new user into the system
```
http://127.0.0.1:5000/api/v1/register
```
*login the registered user in the system
```
http://127.0.0.1:5000/api/v1/login
```
*type as many entries as you'd prefer in the diary
```
http://127.0.0.1:5000/api/v1/make_entry
```
*view all entries you have posted
```
http://127.0.0.1:5000/api/v1/get_all
```
*modify an entry by typing the entry number in place of entryID
```
http://127.0.0.1:5000/api/v1/modify_entry/<int:entryID>
```
*delete an entry by typing the entry number in place of entryID
```
http://127.0.0.1:5000/api/v1/delete_entry/<int:entryID>
```
*logout from the diary
```
http://127.0.0.1:5000/api/v1/logout
```


## Built With

* [Sublime Text](http://www.sublimetext.com/) - The python text editor used
* [Postman](https://www.getpostman.com/) - For testing the end points

## Authors

* **Brian Ryb Okuku** 
