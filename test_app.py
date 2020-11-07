
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Actor, Movie, setupDb, db


class CastingTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.castassist = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InM1OXB5aDZTb0hDZ1NOVzhpS3VuciJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmdhcHAudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmOWM5MThkOTk1MTk3MDA2ODA0ZTc0YyIsImF1ZCI6ImNhc3RpbmdhcGkiLCJpYXQiOjE2MDQ3MTA0MjIsImV4cCI6MTYwNDc5NjgyMiwiYXpwIjoiTDVUaHFJaEhJeVhtMWdWVUxtQnhydkd1eDFhOVdsZ3QiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.K0eYhsERN5uXLle3L4Bt5a1y3fS98pZxJTBtCOstkHQOGY1ZcKC5u8NnuHGuj5fovcfwqtvT2T52aE4w2B0DEVXMZtn6pqM-YcBLbyznYUuKQ67xRmuySLYr-UTbBwjPt4Qr6xDWpZp9JSGdOO2QCCp11a5cUYqdAEB7j8OImA4pkAsHnPiDJvGSC6EIHPQARp-suklew_D2mJzhGp_lZBAzZ25o0eDTt5NgBTk59zEqxQpinPk5J6Fwt-P38WmYPGKWsYoakmT4Z_zC3hJ8rzuK62NFJtTg0bVJW2kWiEl35nMSJiPxpFjpAJoX8iiNbz3kT8_eKhRrAr2-mLnYWg'}
        self.castdirect = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InM1OXB5aDZTb0hDZ1NOVzhpS3VuciJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmdhcHAudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYTMxZWZkY2RkNmM5MDA3MWNhMzY1NCIsImF1ZCI6ImNhc3RpbmdhcGkiLCJpYXQiOjE2MDQ3MTAzNzgsImV4cCI6MTYwNDc5Njc3OCwiYXpwIjoiTDVUaHFJaEhJeVhtMWdWVUxtQnhydkd1eDFhOVdsZ3QiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvciJdfQ.NPJ6oYx6EtABmqzUgUR_G2Cl3BSYEpYECd_Z0llenhDG16MS56_H-uGjLhRqbzUKfqCTLhZV3TF7eGXvE8H5607rae-T9KejqFXY9ycieK0lyfIPJCOUSusdmCBk-7y3Vepn4EjNLkwJWGOcQ8tmq64OVtH5RbPfL8QUQaTdy2UaX-A1XLV7hoUwGjGZsIn-5H1-fpobEqWdU7dGVGduk9gf4WM29WQNqKVswY1Gg4dmStERXFzMEyu2ChUTxN8sbEpnw9tlAteB009AeHg8ub6q1iEKZnjQMqsE1fKBH_KdNQYdFj5VC0SqdLI35dmWqlgWlWVH5IRf-fZocqJK5w'}
        self.execprod = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InM1OXB5aDZTb0hDZ1NOVzhpS3VuciJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmdhcHAudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYTMxZjJhOWU5MzdmMDA2OGM0MDQ1ZCIsImF1ZCI6ImNhc3RpbmdhcGkiLCJpYXQiOjE2MDQ3MTAzMjEsImV4cCI6MTYwNDc5NjcyMSwiYXpwIjoiTDVUaHFJaEhJeVhtMWdWVUxtQnhydkd1eDFhOVdsZ3QiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.GkKoF_rz_FMyk_W4D-_t7UsVBmfBosXq3oqeNlSyTu7djA4LZXNvZZpxgB7wP1QXRV3g8JwqgDqpAo_EwpeftCfqodvPcvt9KVI3NjTGn8_SUgLCJuSHgb_FrcFjiw7-p_-MA3_mFN2wPeYVYAzxSs-T2rxPG-Sy-p64aXAeDVR1MGsGXNQcKygwfwAyLQlZRP9pI8diZTCyQpTT2rntm_DCQKbZSe4d2mXws7D-WAkzjCAsWb-MHBAVKRrLdgfMc6fIdkr5WxwqqfN51rTsuccKaDRfhdMcErAulgYasxv7guPFDzOX-LMPg6dhVLEMruZzpDTOnMgytKQfIyYQDw'}
        self.client = self.app.test_client
        self.database_name = "unittest.db"
        setupDb(self.app, self.database_name)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_getAllActors_success(self):
        res = self.client().get('/api/actors', headers=self.castassist)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_getAllMovies_success(self):
        res = self.client().get('/api/movies', headers=self.castassist)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        
    def test_addActor_success(self):
        res = self.client().post('/api/actors', json={'name': 'bruce lee', 'age':'32', 'gender':'Male'}, headers=self.execprod)
        data = json.loads(res.data)
        self.assertTrue(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_addMovie_success(self):
        res = self.client().post('/api/movies', json={'title':'King of Iron Fist', 'release_date':'4-20-14', 'actor_id': '3'}, headers=self.execprod)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200) 
        
    def test_modActor_success(self):
        res = self.client().patch('/api/actors/1', json={'name':'Harun'}, headers=self.execprod)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_modMovie_success(self):
        res = self.client().patch('/api/movies/5', json={'title':'How to remain steadfast in the jungle'}, headers=self.execprod)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_delActor_success(self):
        res = self.client().delete('/api/actors/9', headers=self.execprod)
        data = json.loads(res.data)
        self.assertTrue(data['success'])

    def test_delMovie_success(self):
        res = self.client().delete('/api/movies/11', headers=self.execprod)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
    
    def test_getAllActors_failure(self):
        res = self.client().get('/api/actors', headers=self.castassist)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_getAllMovies_failure(self):
        res = self.client().get('/api/movies', headers=self.castassist)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        
    def test_addActor_failure(self):
        res = self.client().post('/api/actors', json={'name': 'brandon lee', 'age':'35', 'gender':'Male'}, headers=self.castassist)
        data = json.loads(res.data)
        self.assertEqual(len(data), 0)

    def test_addMovie_failure(self):
        res = self.client().post('/api/movies', json={'title':'Tekken tournament', 'release_date':'4-10-14', 'actor_id': '1'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200) 
        
    def test_modActor_failure(self):
        res = self.client().patch('/api/actors/1', headers=self.execprod)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_modMovie_failure(self):
        res = self.client().patch('/api/movies/6', json={'title':'How to remain steadfast in the jungle'}, headers=self.execprod)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    def test_delActor_failure(self):
        res = self.client().delete('/api/actors/s', headers=self.execprod)
        data = json.loads(res.data)
        self.assertTrue(data['success'])

    def test_delMovie_failure(self):
        res = self.client().delete('/api/movies/7', headers=self.castassist)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
    
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()