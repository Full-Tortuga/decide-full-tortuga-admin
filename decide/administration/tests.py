from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient

from voting.models import Voting, QuestionOption, Question
from census.models import Census
from base.models import Auth, Key

# Create your tests here.

base_url = "/administration/api"

user_json_mock = {
    "username": "mock",
    "password": "qwerty",
    "email": "mock@mock.com",
    "first_name": "mock",
    "last_name": "mock",
}

user_json_mock_updated = {
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
question_json_mock = {
    "id": 1,
    "desc": "Test description",
    "options": [
        {"number": 1, "option": "Test option 1"},
        {"number": 2, "option": "Test option 2"}
    ]
}

question_json_mock_updated = {
    "id": 1,
    "desc": "Test description updated",
    "options": [
        {"number": 1, "option": "Test option 1 updated"},
        {"number": 2, "option": "Test option 2 updated"}
    ]
}

question_json_mock_delete = {
        "desc": "Test description delete",
        "options": [
            {"number": 1, "option": "Test option 1 delete"},
            {"number": 2, "option": "Test option 2 delete"}
    ]
}
census_json_mock = {
    "voting_id": 1,
    "voter_id": 1
}

census_json_mock_updated = {
    "voting_id": 2,
    "voter_id": 2
}

census_json_mock_delete = {
    "voting_id": 1,
    "voter_id": 1
}

def create_voting(self):
    response = self.client.post(base_url + "/votings",
                                voting_json_mock, format='json')
    self.assertEqual(response.status_code, 201)

    return response


def create_auth(self, data=auth_json_mock):
    response = self.client.post(base_url + "/base/auth",
                                data, format='json')
    self.assertEqual(response.status_code, 201)

    return response


def create_user(self):
    response = self.client.post(base_url + "/users",
                                user_json_mock, format='json')
    self.assertEqual(response.status_code, 201)

    return response


def create_key(self):
    response = self.client.post(base_url + "/base/key",
                                {
                                    "p": 9945,
                                    "g": 7876878768,
                                    "y": 876254876254,
                                    "x": 675
                                }, format='json')
    self.assertEqual(response.status_code, 201)

    return response


def create_question(self):
    response = self.client.post(base_url + "/votings/question",
                                 question_json_mock, format="json")
    self.assertEqual(response.status_code, 201)
    return response


def create_census(self):
    response = self.client.post(base_url + "/census",
                                census_json_mock, format="json")
    self.assertEqual(response.status_code, 201)
    return response

class AdministrationTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()

        admin_mock = User(username="admin",
                          email="a@admin.com", is_superuser=True)
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

    # ! DASHBOARD TESTS
    def test_get_dashboard_api(self):
        url = base_url + '/dashboard'
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['votings'], {
            "notStarted": 0, "inProgress": 0, "finished": 0})
        self.assertEqual(response.data['users'], {
            "active": 1, "admins": 1, "employees": 0, "total": 1})

    # ! USER TESTS
    def test_create_user_api(self):
        response = create_user(self)
        db_user = User.objects.get(username="mock")

        self.assertTrue(db_user)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(db_user.username, user_json_mock['username'])
        self.assertEqual(db_user.email, user_json_mock['email'])
        self.assertEqual(db_user.first_name, user_json_mock['first_name'])
        self.assertEqual(db_user.last_name, user_json_mock['last_name'])
        self.assertEqual(db_user.is_active, True)
        self.assertEqual(db_user.is_superuser, False)
        self.assertEqual(db_user.is_staff, False)

    def test_get_users_api(self):
        create_user(self)

        url = base_url + '/users'
        response = self.client.get(url, format="json")
        user_count = User.objects.count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), user_count)

    def test_update_user_api(self):
        create_user(self)
        db_user_id = User.objects.get(username="mock").id

        url = base_url + '/users/' + str(db_user_id)
        response = self.client.put(url, user_json_mock_updated, format="json")
        self.assertEqual(response.status_code, 200)

        db_user = User.objects.get(username="updated")
        self.assertEquals(db_user.id, db_user_id)
        self.assertEqual(db_user.username, user_json_mock_updated['username'])
        self.assertEqual(db_user.email, user_json_mock_updated['email'])
        self.assertEqual(db_user.first_name,
                         user_json_mock_updated['first_name'])
        self.assertEqual(db_user.last_name,
                         user_json_mock_updated['last_name'])
        self.assertEqual(db_user.is_active, True)
        self.assertEqual(db_user.is_superuser, False)
        self.assertEqual(db_user.is_staff, False)

    def test_update_user_state_api(self):
        create_user(self)
        db_user_id = User.objects.get(username="mock").id

        data = {
            "idList": [db_user_id],
            "state": "Active",
            "value": "False"
        }
        url = base_url + "/users/state"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)

        data = {
            "idList": [db_user_id],
            "state": "Staff",
            "value": "True"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)

        data = {
            "idList": [db_user_id],
            "state": "Superuser",
            "value": "True"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)

        db_user = User.objects.get(username="mock")
        self.assertTrue(db_user.is_superuser)
        self.assertTrue(db_user.is_staff)
        self.assertFalse(db_user.is_active)

    def test_delete_user_api(self):
        create_user(self)
        self.assertEqual(User.objects.count(), 2)
        db_user_id = User.objects.get(username="mock").id

        url = base_url + '/users/' + str(db_user_id)
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.count(), 1)

    def test_bulk_delete_users_api(self):
        create_user(self)
        self.assertEqual(User.objects.count(), 2)
        db_user_id = User.objects.get(username="mock").id

        data = {
            "idList": [db_user_id]
        }
        url = base_url + '/users'
        response = self.client.delete(url, data, format="json")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.count(), 1)

    # ! VOTING TESTS
    def test_post_voting_api(self):
        response = create_voting(self)
        db_voting = Voting.objects.last()

        self.assertEqual(response.status_code, 201)
        self.assertTrue(db_voting)
        self.assertEqual(Voting.objects.count(), 1)
        self.assertEqual(db_voting.desc, voting_json_mock.get("desc"))
        self.assertEqual(db_voting.question.desc,
                         voting_json_mock.get("question").get("desc"))
        options = QuestionOption.objects.all().filter(
            question__pk=db_voting.question.id)
        self.assertEqual(options.count(), 3)
        self.assertEqual(db_voting.auths.all().first().url,
                         voting_json_mock.get("auth"))
        censuss = Census.objects.filter(voting_id=db_voting.id)
        self.assertEqual([census.voter_id for census in censuss], [1])

        url = base_url + "/votings"
        response = self.client.post(url,
                                    {"question": ""}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_get_voting_api(self):
        create_voting(self)

        url = base_url + "/votings"
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Test voting")
        self.assertEqual(response.data[0]['desc'], "Test description")

    def test_update_voting_api(self):
        create_voting(self)
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
        options = QuestionOption.objects.all().filter(
            question__pk=db_voting.question.id)
        self.assertEqual(options.count(), 2)
        self.assertEqual(db_voting.auths.all().first().url, data.get("auth"))
        censuss = Census.objects.filter(voting_id=db_voting.id)
        self.assertEqual([census.voter_id for census in censuss], [1])

        response = self.client.put(url,
                                   {"name": "hola", "desc": ""}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_delete_voting_api(self):
        create_voting(self)
        db_voting = Voting.objects.last()
        url = base_url + "/votings/" + str(db_voting.id) + "/"
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Voting.objects.filter(id=db_voting.id).count(), 0)

    # ! KEY TESTS
    def test_post_key_api(self):
        response = create_key(self)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Key.objects.count(), 1)
        self.assertEqual(Key.objects.last().p, 9945)

    def test_get_keys_api(self):
        create_key(self)

        url = base_url + "/base/key"
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['p'], 9945)

    def test_bulk_delete_keys_api(self):
        create_key(self)
        self.assertEqual(Key.objects.count(), 1)

        data = {
            "idList": [Key.objects.last().id]
        }
        url = base_url + "/base/key"
        response = self.client.delete(url, data, format="json")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Key.objects.count(), 0)

    def test_delete_key_api(self):
        create_key(self)
        self.assertEqual(Key.objects.count(), 1)

        db_key = Key.objects.last()
        url = base_url + "/base/key/" + str(db_key.id)
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Key.objects.count(), 0)

    def test_update_key_api(self):
        create_key(self)
        db_key = Key.objects.last()
        url = base_url + "/base/key/" + str(db_key.id)
        data = {
            "p": 5000,
            "g": 7878787878,
            "y": 8732482384744,
            "x": 670
        }
        response = self.client.put(url, data, format="json")

        db_key = Key.objects.last()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(db_key)
        self.assertEqual(db_key.p, 5000)
        self.assertEqual(db_key.g, 7878787878)
        self.assertEqual(db_key.y, 8732482384744)
        self.assertEqual(db_key.x, 670)

    #!AUTH TESTS
    def test_get_list_auth_api(self):
        create_auth(self)
        url = base_url + "/base/auth"
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), Auth.objects.count())
        self.assertEqual(response.data[len(response.data) - 1]['name'], "pruebaeeww")
        self.assertEqual(response.data[len(response.data) - 1]['url'], "http://localhost:8000")
        self.assertEqual(response.data[len(response.data) - 1]['me'], True)

    def test_get_auth_api(self):
        create_auth(self)
        db_auth = Auth.objects.last()
        url = base_url + "/base/auth/" + str(db_auth.id)
        response = self.client.get(url, format="json")
        self.assertEqual(response.data['name'], "pruebaeeww")
        self.assertEqual(response.data['url'], "http://localhost:8000")
        self.assertEqual(response.data['me'], True)

    def test_post_auth_api(self):
        create_auth(self)
        db_auth = Auth.objects.last()
        self.assertEqual(auth_json_mock.get('name'), db_auth.name)
        self.assertEqual(auth_json_mock.get('url'), db_auth.url)
        self.assertEqual(auth_json_mock.get('me'), db_auth.me)

        url = base_url + "/base/auth"
        response = self.client.post(url,
                                    {"name": "hola"}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_put_auth_api(self):
        create_auth(self)
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
        create_auth(self)
        db_auth = Auth.objects.last()

        url = base_url + "/base/auth/" + str(db_auth.id)
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Voting.objects.filter(id=db_auth.id).count(), 0)

    def test_bulk_delete_auth_api(self):
        create_auth(self)
        create_auth(self, auth_json_mock_delete)
        db_auth_id = Auth.objects.last().id

        url = base_url + "/base/auth"
        id_list = [db_auth_id, db_auth_id - 1]
        response = self.client.delete(url, {"idList": id_list}, format="json")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Voting.objects.filter(id__in=id_list).count(), 0)

        create_auth(self)
        create_auth(self, auth_json_mock_delete)

        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Voting.objects.count(), 0)

    #! QUESTION TESTS
    def test_get_list_question_api(self):
        create_question(self)
        url = base_url + "/votings/question"
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), Question.objects.count())
        self.assertEqual(response.data[len(response.data) - 1]['desc'], "Test description")
        self.assertEqual(response.data[len(response.data) - 1]['options'][0].get("option"), "Test option 1")
        self.assertEqual(response.data[len(response.data) - 1]['options'][1].get("option"), "Test option 2")
        self.assertEqual(response.data[len(response.data) - 1]['options'][0].get("number"), 1)
        self.assertEqual(response.data[len(response.data) - 1]['options'][1].get("number"), 2)

    def test_get_question_api(self):
        create_question(self)
        db_question = Question.objects.last()

        url = base_url + "/votings/question/" + str(db_question.id) +"/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.data['desc'], "Test description")
        self.assertEqual(response.data['options'][0].get("option"), "Test option 1")
        self.assertEqual(response.data['options'][1].get("option"), "Test option 2")
        self.assertEqual(response.data['options'][0].get("number"), 1)
        self.assertEqual(response.data['options'][1].get("number"), 2)


    def test_post_question_api(self):
        create_question(self)
        db_question = Question.objects.last()
        self.assertEqual(db_question.desc, question_json_mock.get("desc"))
        options = QuestionOption.objects.all().filter(question__pk=db_question.id)
        self.assertEqual(options.count(), 2)

        url = base_url + "/votings/question"
        response = self.client.post(url,
                                    {"desc":"Test description"}, format="json")
        self.assertEqual(response.status_code, 400)


    def test_put_question_api(self):
        create_question(self)
        db_question = Question.objects.last()
        url = base_url + "/votings/question/" + str(db_question.id) + "/"
        response = self.client.put(
            url, question_json_mock_updated, format="json")
        db_question = Question.objects.last()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(question_json_mock_updated.get('desc'), db_question.desc)
        options = QuestionOption.objects.all().filter(question__pk=db_question.id)
        self.assertEqual(question_json_mock_updated.get('options')[0]["option"], options.values("option")[0]["option"])
        self.assertEqual(question_json_mock_updated.get('options')[1]["option"], options.values("option")[1]["option"])

        response = self.client.put(url,
                                   {"desc": "Test description 1 update"}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_delete_question_api(self):
        create_question(self)
        db_question = Question.objects.last()

        url = base_url + "/votings/question/" + str(db_question.id) + "/"
        response = self.client.delete(url, format = "json")

        self.assertEqual(response.status_code,204)
        self.assertEqual(Question.objects.filter(id=db_question.id).count(),0)

    def test_bulk_delete_question_api(self):
        create_question(self)
        self.assertEqual(Question.objects.count(), 1)

        data = {
            "idList": [Question.objects.last().id]
        }
        url = base_url + "/votings/question"
        response = self.client.delete(url, data, format="json")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Question.objects.count(), 0)

        #! CENSUS TESTS
    def test_get_list_census_api(self):
        create_census(self)
        url = base_url + "/census"
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), Census.objects.count())
        self.assertEqual(response.data[len(response.data) - 1]['voting_id'], 1)
        self.assertEqual(response.data[len(response.data) - 1]['voter_id'], 1)

    def test_get_census_api(self):
        create_census(self)
        db_census = Census.objects.last()

        url = base_url + "/census/" + str(db_census.id)
        response = self.client.get(url, format="json")
        self.assertEqual(response.data['voting_id'], 1)
        self.assertEqual(response.data['voter_id'], 1)

    def test_post_census_api(self):
        create_census(self)
        db_census = Census.objects.last()
        self.assertEqual(db_census.voting_id, census_json_mock.get("voting_id"))
        self.assertEqual(db_census.voter_id, census_json_mock.get("voter_id"))

        url = base_url + "/census"
        response = self.client.post(url,
                                    {"desc":"Test description"}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_put_census_api(self):
        create_census(self)
        db_census = Census.objects.last()
        url = base_url + "/census/" + str(db_census.id)
        response = self.client.put(
            url, census_json_mock_updated, format="json")
        db_census = Census.objects.last()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(census_json_mock_updated.get('voting_id'), db_census.voting_id)
        self.assertEqual(census_json_mock_updated.get('voter_id'), db_census.voter_id)

        response = self.client.put(url,
                                   {"voting_id": 2}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_delete_census_api(self):
        create_census(self)
        db_census = Census.objects.last()

        url = base_url + "/census/" + str(db_census.id)
        response = self.client.delete(url, format = "json")

        self.assertEqual(response.status_code,204)
        self.assertEqual(Census.objects.filter(id=db_census.id).count(),0)

    def test_bulk_delete_census_api(self):
        create_census(self)
        self.assertEqual(Census.objects.count(), 1)

        data = {
            "idList": [Census.objects.last().id]
        }
        url = base_url + "/census"
        response = self.client.delete(url, data, format="json")
        self.assertEqual(Census.objects.count(), 0)


