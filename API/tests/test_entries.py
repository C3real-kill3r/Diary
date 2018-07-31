import os,sys

sys.path.insert(0, os.path.abspath(".."))

from flask import *
import unittest
import json
from __init__ import *

class Test_Entries(unittest.TestCase):
    def setUP(self):
        self.app=app.test_client()

    def test_home(self):
        with app.test_client() as h:
            response = h.get('/')
            self.assertEqual(response.status_code, 404)
        with app.test_client() as h:
            response = h.get('/ap1/v2/')
            self.assertEqual(response.status_code, 404)

    def test_view_all(self):
        with app.test_client() as c:
            response= c.get('/api/v2/view_all',)
            self.assertEqual(response.status_code, 403)

    def test_make_entry(self):
        testr = app.test_client()
        self.assertEqual(testr.post('/api/v2/make_entry', json={"title":"brybz", "comment":"1234",}).status_code, 403)

    def test_comment_view_one(self):
        with app.test_client() as cs:
            response = cs.get('/api/v2/view_one/1',)
            kk = cs.get('/ap1/v2/view_one/1')
            self.assertEqual(response.status_code, 500)
            self.assertEqual(kk.status_code, 404)

    def test_modify_entry(self):
        with app.test_client() as me:
            self.assertEqual(me.get('/api/v2/modify_entry').status_code, 404)
            self.assertEqual(me.get('/api/v2/modify_entry/1').status_code, 405)

if __name__ == '__main__':
    unittest.main()