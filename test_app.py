
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
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InM1OXB5aDZTb0hDZ1NOVzhpS3VuciJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmdhcHAudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmOWM5MThkOTk1MTk3MDA2ODA0ZTc0YyIsImF1ZCI6ImNhc3RpbmdhcGkiLCJpYXQiOjE2MDQ0OTU0MjksImV4cCI6MTYwNDU4MTgyOSwiYXpwIjoiTDVUaHFJaEhJeVhtMWdWVUxtQnhydkd1eDFhOVdsZ3QiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.JdvDBqgBi5ECD9Wlr-iX2VB4jvvRM68JBZohP2VBtBccxh91UCTbNYrbe8xkZ0s1Zy_G0V8lgw9bGu9daaH1tUYPirRsx2mvJv36YVQErsrPDD_OxJTKBKSkFW8LF70b02vEQxWE0d2_h4GGrlyAsEmDD9vtp3nyNukSBItBqJK52kzF2XZvJLGW31IYpdTH1A4Dge02l1tDUOgJ2PNagIpYaDtZfZ8T7sI82l_xbHnHXYpZhIc7H1GV5Tjlbn83p3_Nai8z9s_tuHn36jSGbuIGLXNs76YGl3Ery4iuVIFuW86PJBA1MRKr3ljKDugA3xdgaUzagrFsr9JzFwFYew'}
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

    def test_getAllActors(self):
        res = self.client().get('/api/actors', headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    # def test_getAllQuestions(self):
    #     res = self.client().get('/api/questions')
    #     data = json.loads(res.data)
    #     self.assertEqual(data['success'], True)
    #     self.assertIsNotNone(data['current_category'])
    
    # def test_deleteQuestion(self):
    #     res = self.client().delete('/api/questions/1')
    #     data = json.loads(res.data)
    #     self.assertEqual(data['question_id'], 1)
    #     self.assertNotEqual(data['success'], True)

    # def test_insertQuestion(self):
    #     res = self.client().post('/api/questions', json={'question':'What book is the most valuable on earth ?', 'answer':'The Quran','category':'knowledge','difficulty':'1'})
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['question_id'], '')
    
    # def test_searchQuestion(self):
    #     res = self.client().post('/api/questions/search', json={'searchTerm':'fastest'})
    #     data = json.loads(res.data)
    #     self.assertNotEqual(data['questions'], '')
    #     self.assertEqual(res.status_code, 404)

    # def test_getCategoryQuestions(self):
    #     res = self.client().get('/api/categories/1/questions')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertLess(data['total_questions'], 0)

    # def test_quizzQuestions(self):
    #     res = self.client().post('/api/quizzes', json={'previous_questions':[], 'quiz_category':{'type':'web','id':'1'}})
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['question'], '')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()