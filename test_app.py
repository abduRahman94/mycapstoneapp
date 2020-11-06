
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
        self.castassist = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InM1OXB5aDZTb0hDZ1NOVzhpS3VuciJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmdhcHAudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmOWM5MThkOTk1MTk3MDA2ODA0ZTc0YyIsImF1ZCI6ImNhc3RpbmdhcGkiLCJpYXQiOjE2MDQ2NzkyNTcsImV4cCI6MTYwNDc2NTY1NywiYXpwIjoiTDVUaHFJaEhJeVhtMWdWVUxtQnhydkd1eDFhOVdsZ3QiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.dd4NSs9aApKtgL0zZdj2BQPFfVInZS_tVfQotIanfdR6301Xl_xxGBbQV4CEw6XN9ETnvT4AjqGxSuONztA9tAQPg5Da4H2T9gpdCukNlwArcGuwYXdR8P4lB2Rw4omiNgO9KqrzWTX9E-2vWg6Qpnb_kcYaBqyxdLqI3dSIEnnBmU2_JVlQSJo-xyHbid2Yc2P80nQirhMysGyzfOe13-EoDYjhexlAr2wUnT2vCz7Jrpibu5baSfK7SXmfF8JmwYHMNWpsLxr8grOvGhvafsmBvwjOAcdodvhWJRx3a6SssFdVXsjlo9GYlBEZ_Y5ixCnxzRfhTF0HJ8-tctFkgw'}
        self.castdirect = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InM1OXB5aDZTb0hDZ1NOVzhpS3VuciJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmdhcHAudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYTMxZWZkY2RkNmM5MDA3MWNhMzY1NCIsImF1ZCI6ImNhc3RpbmdhcGkiLCJpYXQiOjE2MDQ2NzkyMDgsImV4cCI6MTYwNDc2NTYwOCwiYXpwIjoiTDVUaHFJaEhJeVhtMWdWVUxtQnhydkd1eDFhOVdsZ3QiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvciJdfQ.YTx4n-H0nA9Z-MJ3KjMVtuh99-6mZESE42MK8CkGeJ-fwfB2-93MurzPx8vdXfiLt6WDeXK7cNF_6ioO6-brP7Mo9BGgo2hbLtUyHDSVqRJtNX-I2M6uKW4eBfwjt7flYToA8relb2AiAHYW_ehcsBJPowkAV2jAcHpCgsT6NQUOelo3ejCXfPPdVaCMEwkHFpmHNa8Xnn5WzAfmSG9WIgdf7asMDB8_NivQt96IgeqNzYEolAJjeNOqk663889mMhe41HYmybQrMiWdF6NFgz7lVsxFdL69dPOGnzjXPqmba7XDonbUOuWBCwAcSq_rhfjn5EYSUOJaG_iKVvkAZQ'}
        self.execprod = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InM1OXB5aDZTb0hDZ1NOVzhpS3VuciJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmdhcHAudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYTMxZjJhOWU5MzdmMDA2OGM0MDQ1ZCIsImF1ZCI6ImNhc3RpbmdhcGkiLCJpYXQiOjE2MDQ2NzkxNjcsImV4cCI6MTYwNDc2NTU2NywiYXpwIjoiTDVUaHFJaEhJeVhtMWdWVUxtQnhydkd1eDFhOVdsZ3QiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.q_MJK64PfexXJiUvcQSIyrH1CdsP0iGC4F-1KuuscgoO5s5DLbm9f4S-JxYNDTHS6m952_dRzDE9SzCvtlzoUdyLzwPhIRq1LWEEdEZM8QRfhhUJrY0NLLIVBOCaxAKmISc3DIC-JA3bIonLwFZ6B8h9lpJR3LhI7AOdoBIxz7EEPX3Z7ymoplZdE3QIDg4jJNNfeaIAjurl-YCc41oqSLGx0WdjO8kSP1NhZxi9w7HxA0I3cyEl6CMAldg1BarHrmsYHv4rywVIeQqGtBySO_Cw_fovec2L6Y3UuB8ZI1OgbeSLfmQegiGHmEUrMWeLUIa2WFpLNq5CTjO4ZhThbg'}
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