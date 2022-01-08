from django.contrib.auth.models import User
from .serializers import AdminVotingGetSerializer
from voting.models import Voting

from rest_framework.test import APITestCase, APIClient


# Create your tests here.

base_url = "/administration/api"

user_json_mock = {
    "username": "admin",
    "password": "qwerty",
    "email": "ad@admin.com",
    "first_name": "admin",
    "last_name": "admin",
}

user_json_mock_updated = {
    "id": 1,
    "username": "updated",
    "password": "updated",
    "email": "updated@admin.com",
    "first_name": "updated",
    "last_name": "updated",
}

voting_json_mock = {
    "name": "Test voting",
    "desc": "Test description",
    "question": {
        "desc": "Test question",
            "options": [
                {"number": 1, "option": "Test option 1"},
                {"number": 2, "option": "Test option 2"},
                {"number": 3, "option": "Test option 3"}
            ]
    },
    "auth": "http://localhost:8000",
    "census": [1]
}

voting_json_mock_updated = {
    "id": 1,
    "name": "Test updated voting",
    "desc": "Test updated voting description",
    "question": {
        "desc": "Test updated question",
        "options": [
            {"number": 1, "desc": "Test option 1"},
            {"number": 2, "desc": "Test option 2"},
        ]
    },
    "auth": "http://localhost:8080",
            "census": [1]
}


def create_voting(self):
    response = self.client.post(base_url + "/voting/",
                                voting_json_mock, format='json')
    return response


class AdministrationTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()

        admin_mock = User(username="admin", is_superuser=True)
        admin_mock.set_password("qwerty")
        admin_mock.save()

        url = base_url + "/auth/login"
        data = {'username': "admin", 'password': "qwerty"}
        response = self.client.post(url, data, format="json")
        self.token = response.cookies.get('token', "")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.token)

    def tearDown(self):
        super().tearDown()

        url = base_url + "/auth/logout"
        response = self.client.get(url, format="json")
        self.token = response.cookies.get('token', "")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.token["expires"],
                         "Thu, 01 Jan 1970 00:00:00 GMT")

    def test_get_dashboard_api(self):
        url = base_url + '/dashboard'
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['votings'], {
                         "notStarted": 0, "inProgress": 0, "finished": 0})
        self.assertEqual(response.data['users'], {
                         "active": 1, "admins": 1, "employees": 0, "total": 1})


'''
    def test_post_voting_api(self):
        response = self.create_voting()
        db_voting = Voting.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(db_voting)
        self.assertEqual(Voting.objects.count(), 1)
        self.assertEqual(db_voting.desc, voting_json_mock.get("desc"))
        self.assertEqual(db_voting.question.desc,
                         voting_json_mock.get("question").get("desc"))
        self.assertEqual(db_voting.question.options.count(), 3)
        self.assertEqual(db_voting.auth, voting_json_mock.get("auth"))
        self.assertEqual(db_voting.census, [1])

    def test_get_voting_api(self):
        self.create_voting()

        url = base_url + "/votings"
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['name'], "Test voting")
        self.assertEqual(response.data[0]['desc'], "Test description")

    def test_update_voting_api(self):
        self.create_voting()

        url = base_url + "/votings/1"
        data = voting_json_mock_updated
        response = self.client.put(
            url, voting_json_mock_updated, format="json")
        db_voting = Voting.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(db_voting)
        self.assertEqual(db_voting.desc, data.get("desc"))
        self.assertEqual(db_voting.question.desc,
                         data.get("question").get("desc"))
        self.assertEqual(db_voting.question.options.count(), 2)
        self.assertEqual(db_voting.auth, data.get("auth"))
        self.assertEqual(db_voting.census, [1])

    def test_delete_voting_api(self):
        self.create_voting()

        url = base_url + "/votings/1"
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Voting.objects.count(), 0)

'''
