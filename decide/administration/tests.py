from django.contrib.auth.models import User

from base.models import Auth
from census.models import Census
from .serializers import AdminVotingGetSerializer
from voting.models import Voting, QuestionOption
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
auth_json_mock = {
    "name": "pruebaeeww",
    "url": "http://localhost:8000",
    "me": True
}

auth_json_mock_update = {
    "name": "update",
    "url": "http://localhost:3000",
    "me": False
}

auth_json_mock_delete = {
    "name": "pruebaeeww2222",
    "url": "http://localhost:9000",
    "me": False
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
            {"number": 1, "option": "Test option 1"},
            {"number": 2, "option": "Test option 2"},
        ]
    },
    "auth": "http://localhost:8080",
    "census": [1]
}


class AdministrationTestCase(APITestCase):
    def create_voting(self):
        url = base_url + "/votings"
        response = self.client.post(url,
                                    voting_json_mock, format='json')
        return response

    def create_auth(self, data=auth_json_mock):
        url = base_url + "/base/auth"
        response = self.client.post(url,
                                    data, format='json')
        return response

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

    def test_post_voting_api(self):
        response = self.create_voting()
        db_voting = Voting.objects.last()

        self.assertEqual(response.status_code, 201)
        self.assertTrue(db_voting)
        self.assertEqual(Voting.objects.count(), 1)
        self.assertEqual(db_voting.desc, voting_json_mock.get("desc"))
        self.assertEqual(db_voting.question.desc,
                         voting_json_mock.get("question").get("desc"))
        options = QuestionOption.objects.all().filter(question__pk=db_voting.question.id)
        self.assertEqual(options.count(), 3)
        self.assertEqual(db_voting.auths.all().first().url, voting_json_mock.get("auth"))
        censuss = Census.objects.filter(voting_id=db_voting.id)
        self.assertEqual([census.voter_id for census in censuss], [1])

        url = base_url + "/votings"
        response = self.client.post(url,
                                    {"question": ""}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_get_voting_api(self):
        self.create_voting()

        url = base_url + "/votings"
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Test voting")
        self.assertEqual(response.data[0]['desc'], "Test description")

    def test_update_voting_api(self):
        self.create_voting()
        db_voting = Voting.objects.last()
        url = base_url + "/votings/" + str(db_voting.id) + "/"
        data = voting_json_mock_updated
        response = self.client.put(
            url, voting_json_mock_updated, format="json")
        db_voting = Voting.objects.last()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(db_voting)
        self.assertEqual(db_voting.desc, data.get("desc"))
        self.assertEqual(db_voting.question.desc,
                         data.get("question").get("desc"))
        options = QuestionOption.objects.all().filter(question__pk=db_voting.question.id)
        self.assertEqual(options.count(), 2)
        self.assertEqual(db_voting.auths.all().first().url, data.get("auth"))
        censuss = Census.objects.filter(voting_id=db_voting.id)
        self.assertEqual([census.voter_id for census in censuss], [1])

        response = self.client.put(url,
                                   {"name": "hola", "desc": ""}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_delete_voting_api(self):
        self.create_voting()
        db_voting = Voting.objects.last()
        url = base_url + "/votings/" + str(db_voting.id) + "/"
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Voting.objects.filter(id=db_voting.id).count(), 0)

    def test_get_list_auth_api(self):
        self.create_auth()
        url = base_url + "/base/auth"
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), Auth.objects.count())
        self.assertEqual(response.data[len(response.data) - 1]['name'], "pruebaeeww")
        self.assertEqual(response.data[len(response.data) - 1]['url'], "http://localhost:8000")
        self.assertEqual(response.data[len(response.data) - 1]['me'], True)

    def test_get_auth_api(self):
        self.create_auth()
        db_auth = Auth.objects.last()
        url = base_url + "/base/auth/" + str(db_auth.id)
        response = self.client.get(url, format="json")
        self.assertEqual(response.data['name'], "pruebaeeww")
        self.assertEqual(response.data['url'], "http://localhost:8000")
        self.assertEqual(response.data['me'], True)

    def test_post_auth_api(self):
        self.create_auth()
        db_auth = Auth.objects.last()
        self.assertEqual(auth_json_mock.get('name'), db_auth.name)
        self.assertEqual(auth_json_mock.get('url'), db_auth.url)
        self.assertEqual(auth_json_mock.get('me'), db_auth.me)

        url = base_url + "/base/auth"
        response = self.client.post(url,
                                    {"name": "hola"}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_put_auth_api(self):
        self.create_auth()
        db_auth = Auth.objects.last()
        url = base_url + "/base/auth/" + str(db_auth.id)
        response = self.client.put(
            url, auth_json_mock_update, format="json")
        db_auth = Auth.objects.last()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(auth_json_mock_update.get('name'), db_auth.name)
        self.assertEqual(auth_json_mock_update.get('url'), db_auth.url)
        self.assertEqual(auth_json_mock_update.get('me'), db_auth.me)

        response = self.client.put(url,
                                   {"name": "hola"}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_delete_auth_api(self):
        self.create_auth()
        db_auth = Auth.objects.last()

        url = base_url + "/base/auth/" + str(db_auth.id)
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Voting.objects.filter(id=db_auth.id).count(), 0)

    def test_bulk_delete_auth_api(self):
        self.create_auth()
        self.create_auth(auth_json_mock_delete)
        db_auth_id = Auth.objects.last().id

        url = base_url + "/base/auth"
        id_list = [db_auth_id, db_auth_id - 1]
        response = self.client.delete(url, {"idList": id_list}, format="json")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Voting.objects.filter(id__in=id_list).count(), 0)

        self.create_auth()
        self.create_auth(auth_json_mock_delete)

        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Voting.objects.count(), 0)
