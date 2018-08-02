import os,sys

sys.path.insert(0, os.path.abspath(".."))

import unittest
import psycopg2
import json
from __init__ import *

class Test_Users(unittest.TestCase):

    def setUp(self):
        connection = psycopg2.connect(dbname='travis', user='travis', host='localhost', password='test', port='5432')
        with connection.cursor() as cursor:
            cursor.execute ("CREATE TABLE IF NOT EXISTS entries (entryID serial PRIMARY KEY,\
                username varchar(200) NOT NULL, title varchar(50) NOT NULL,\
                comment text NOT NULL,comment_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)")
            cursor.execute ("CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY,\
                fname varchar(100), lname varchar(100),username varchar(100) NOT NULL,\
                email varchar(100) NOT NULL,password varchar(100) NOT NULL,\
                registration_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)")
            cursor.execute ("INSERT INTO users (fname, lname, username, email, password) VALUES ('brian', 'ryb', 'ken', 'brybzi@gmail.com',\
             '76176fdf71023bf2af126f78ef3b2c4edbb01cd17524d39ed8c214be29ffa2c7')")
        connection.commit()



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
        self.assertEqual(response_data['message'], 'you are succesfully registered') 

    def test_login(self):
        logn = app.test_client()
        self.assertEqual(logn.post('/api/v2/auth/login', json={"username":"brybz", "password":"1234",}).status_code, 200)

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
            self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main()