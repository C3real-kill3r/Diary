import unittest
import json
from run import *

class Test_Diary(unittest.TestCase):

    def test_home(self):
        with app.test_client() as h:
            response = h.get('/api/v2/')
            self.assertEqual(response.status_code, 200)
        with app.test_client() as h:
            response = h.get('/ap1/v2/')
            self.assertEqual(response.status_code, 404)

    def test_comment(self):
        with app.test_client() as c:
            response= c.get('/api/v2/get_all',)
            self.assertEqual(response.status_code, 200)

    def test_comment_single(self):
        with app.test_client() as cs:
            response= cs.get('/api/v2/get_one/1',)
            self.assertEqual(response.status_code, 200)