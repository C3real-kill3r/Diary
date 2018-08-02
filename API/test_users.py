import os,sys

sys.path.insert(0, os.path.abspath(".."))

from flask import *
import unittest
import json
from __init__ import *

class Test_Users(unittest.TestCase):

    client = app.test_client()

    def test_wrong_method(self):
        self.assertEqual(app.test_client().post('/api/v2/').status_code, 405)


    def test_signup(self):
        data = json.dumps({"fname":"brian",
            "lname":"ryb",
            "username":"brybz",
            "email":"brybzi@gmail.com",
            "password":"Zi!123",
            "confirm password":"Zi!123"})
        header = {"content-type" : "application/json"}
        response = self.client.post("api/v2/auth/signup", data=data, headers=header)
        response_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['message'], 'username exists') 

    def test_login(self):
        logn = app.test_client()
        self.assertEqual(logn.post('/api/v2/auth/login', json={"username":"brybz", "password":"1234",}).status_code, 200)

    def test_home(self):
        response = app.test_client().get('/api/v2/')
        self.assertEqual(response.status_code, 200)
        response = app.test_client().get('/ap1/v2/')
        self.assertEqual(response.status_code, 404)

    def test_view_all(self):
        response = app.test_client().get('/api/v2/entries',)
        self.assertEqual(response.status_code, 403)

    def test_logout(self):
        lgout = app.test_client()
        self.assertEqual(lgout.get('/api/v2/logout').status_code, 200)

    def test_comment_view_one(self):
        response= app.test_client().get('/api/v2/entries/1',)
        self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main()