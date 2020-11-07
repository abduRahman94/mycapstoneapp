import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Actor, Movie, setupDb, db

token_castassist = os.environ.get('token_castassist')
token_castdirect = os.environ.get('token_castdirect')
token_execprod = os.environ.get('token_execprod')


class CastingTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.castassist = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token_castassist}
        self.castdirect = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token_castdirect}
        self.execprod = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token_execprod}
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
        res = self.client().post('/api/actors',
                                 json={'name': 'bruce lee',
                                       'age': '32',
                                       'gender': 'Male'},
                                 headers=self.execprod)
        data = json.loads(res.data)
        self.assertTrue(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_addMovie_success(self):
        res = self.client().post('/api/movies',
                                 json={'title': 'King of Iron Fist',
                                       'release_date': '4-20-14',
                                       'actor_id': '3'},
                                 headers=self.execprod)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_modActor_success(self):
        res = self.client().patch('/api/actors/1',
                                  json={'name': 'Harun'},
                                  headers=self.execprod)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_modMovie_success(self):
        res = self.client().patch('/api/movies/5',
                                  json={'title':
                                        '''How to remain
                                        steadfast in the jungle'''},
                                  headers=self.execprod)
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
        res = self.client().post('/api/actors',
                                 json={'name': 'brandon lee',
                                       'age': '35',
                                       'gender': 'Male'},
                                 headers=self.castassist)
        data = json.loads(res.data)
        self.assertEqual(len(data), 0)

    def test_addMovie_failure(self):
        res = self.client().post('/api/movies',
                                 json={'title': 'Tekken tournament',
                                       'release_date': '4-10-14',
                                       'actor_id': '1'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_modActor_failure(self):
        res = self.client().patch('/api/actors/1', headers=self.execprod)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_modMovie_failure(self):
        res = self.client().patch('/api/movies/6',
                                  json={'title': '''How to remain
                                        steadfast in the jungle'''},
                                  headers=self.execprod)
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
