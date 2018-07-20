import unittest
import json
from diary import *

class Test_Diary(unittest.TestCase):
    
    def test_home(self):
        with app.test_client() as h:
            response = h.get('/api/v1/')
            self.assertEqual(response.status_code, 200)
        with app.test_client() as h:
        	response = h.get('/ap1/v1/')
        	self.assertEqual(response.status_code, 404)
   
    def test_comment(self):
        comment=app.test_client()
        response= comment.get('/api/v1/get_all',)
        self.assertEqual(response.status_code, 200)

    def test_comment_single(self):
        scomment=app.test_client()
        self.assertEqual(scomment.get('/api/v1/get_one/1',).status_code, 200)

    def test_register(self):
        with app.test_client() as r:
            response=r.get('/api/v1/register',)
            self.assertEqual(response.status_code, 405)
            self.assertEqual(r.post('/api/v1/login', json={"name":"brian ryb","username":"brybz","email":"brybzi@gmail.com","password":"1234",}).status_code, 200)

    def test_login(self):
        with app.test_client() as l:
            response=l.get('/api/v1/login',)
            self.assertEqual(response.status_code, 405)
            self.assertEqual(l.post('/api/v1/login', json={"username":"brybz","password":"1234"}).status_code, 200)

    def test_make_entry(self):
        with app.test_client() as m:
            response=m.get('/api/v1/login',)
            self.assertEqual(response.status_code, 405)    
            self.assertEqual(m.post('/api/v1/login', json={"entry":"lets try something out"}).status_code, 500)

    def test_logout(self):
        with app.test_client() as lo:
            self.assertTrue(lo.get('/api/v1/logout',).status_code, 200)

    def test_modify_entry(self):
        with app.test_client() as tester:
            self.assertEqual(tester.get('/api/v1/modify_entry/1').status_code, 405)
            self.assertEqual(tester.get('/api/vi/modify_entry/').status_code, 404)



    def test_logout(self):
        with app.test_client() as test:
            response = test.get('/api/v1/logout')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(test.get('/api/v1/get_all').status_code,200)

if __name__=='__main__':
    unittest.main()