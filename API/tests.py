import os,sys

#sys.path.insert(0, os.path.abspath(".."))

from flask import request
import unittest
import json
from __init__ import app

class Test_Entries(unittest.TestCase):
    client = app.test_client()

    def login_user(self):
        data = json.dumps({"username":"ken",
                       "password":"Zi!123"})
        header = {"content-type" : "application/json"}
        login_response = self.client.post("api/v2/auth/login", data=data, headers=header)
        response_data = login_response.get_json()
        return response_data["message"]["token"]

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

    def test_view_all_valid(self):
        token = self.login_user()
        header = { "x-access-token":token}
        response = self.client.get("api/v2/entries", headers=header)
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/api/v2/')
        self.assertEqual(response.status_code, 200)

    def test_view_all(self):
        with app.test_client() as c:
            response= c.get('/api/v2/entries',)
            self.assertEqual(response.status_code, 403)

    def test_make_entry(self):
        testr = app.test_client()
        self.assertEqual(testr.post('/api/v2/entries', json={"title":"brybz", "comment":"1234",}).status_code, 403)

    def test_post_entry(self):
        token = self.login_user()
        data = json.dumps({"title":"A new entry",
                       "comment":"A comment"})
        header = {"content-type" : "application/json", "x-access-token": token}
        response = self.client.post("api/v2/entries", data=data, headers=header)
        response_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["message"], "entry successfully posted!!")

    def test_comment_view_one(self):
        token = self.login_user()
        header = { "x-access-token":token}
        response = self.client.get("api/v2/entries/1", headers=header)
        self.assertEqual(response.status_code, 200)

    def test_modify_entry(self):
        token = self.login_user()
        data = json.dumps({"comment":"A comment 2"})
        header = {"content-type" : "application/json", "x-access-token": token}
        response = self.client.put("api/v2/entries/1", data=data, headers=header)
        response_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["message"], "enrtry does not exist!!")

if __name__ == '__main__':
    unittest.main()