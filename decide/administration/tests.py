from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient


# Create your tests here.
from voting.models import Voting


class AdministrationTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user_admin = User(username='admin', is_staff=True, is_superuser=True)
        user_admin.set_password('qwerty')
        user_admin.save()
        data = {'username': "admin", 'password': "qwerty"}
        response = self.client.post('/administration/api/auth/login', data, format="json")
        self.assertEqual(response.status_code, 200)
        self.token = response.cookies.get('token', "")
        self.assertTrue(self.token)

    def tearDown(self):
        response = self.client.get('/administration/api/auth/logout')
        self.assertEqual(response.status_code, 200)
        self.token = response.COOKIES.get('token', "")
        self.assertFalse(self.token)

    def test_post_voting_api(self):
        data = {
            "name": "test",
            "desc": "test",
            "question": {
                "desc": "test?",
                "options": [
                    {"number": 1,
                     "option": "prueba"},
                    {"number": 2,
                     "option": "no prueba"}]},
            "census": [1],
            "auth": "http://localhost:8000"
        }
        response = self.client.post('/administration/api/votings', data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Voting.objects.all().First() is not None)
