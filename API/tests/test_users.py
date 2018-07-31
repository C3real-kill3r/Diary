import os,sys

sys.path.insert(0, os.path.abspath(".."))

from flask import *
import unittest
import json
from __init__ import *

class Test_Users(unittest.TestCase):


    def test_wrong_method(self):
        self.assertEqual(app.test_client().post('/api/v2/').status_code, 405)


    def test_register(self):
        with app.test_client() as r:
            response = r.get('/api/v2/auth/signup',)
            self.assertEqual(response.status_code, 405)
            self.assertEqual(r.post('/api/v2/auth/signup', json={"fname":"brian", "lname":"ryb","username":"brybz",\
                "email":"brybzi@gmail.com",\
                "password":"1234", "confirm password":"1234"}).status_code, 500) 

    def test_login(self):
        logn = app.test_client()
        self.assertEqual(logn.post('/api/v2/auth/login', json={"username":"brybz", "password":"1234",}).status_code, 500)

    def test_home(self):
        with app.test_client() as h:
            response = h.get('/api/v2/')
            self.assertEqual(response.status_code, 200)
        with app.test_client() as h:
            response = h.get('/ap1/v2/')
            self.assertEqual(response.status_code, 404)

    def test_view_all(self):
        with app.test_client() as c:
            response = c.get('/api/v2/entries',)
            self.assertEqual(response.status_code, 403)

    def test_logout(self):
        lgout = app.test_client()
        self.assertEqual(lgout.get('/api/v2/logout').status_code, 200)

    def test_comment_view_one(self):
        with app.test_client() as cs:
            response= cs.get('/api/v2/entries/1',)
            self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()