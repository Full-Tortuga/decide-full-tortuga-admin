from .models import Census
from base.tests import BaseTestCase


class CensusTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.census = Census(voting_id=1, voter_id=1, type='V')
        self.census.save()

    def tearDown(self):
        super().tearDown()
        self.census = None

    def test_get_all_votings(self):
        # with voting_id=0 we get all votings
        response1 = self.client.get('/census/{}/'.format(0), format='json')
        self.assertEqual(response1.status_code, 200)

        response2 = self.client.get('/census/{}/'.format(1), format='json')
        self.assertEqual(response2.status_code, 200)

        self.assertEqual(response1.json(), response2.json())

    def test_list_voting(self):
        response = self.client.get('/census/?voting_id={}&type=V'.format(1), format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.get('/census/?voting_id={}&type=V'.format(1), format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get('/census/?voting_id={}&type=V'.format(1), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'voters': [1]})

    def test_add_new_voters_conflict(self):
        data = {'voting_id': 1, 'voters': [1], 'type': 'V'}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 409)

    def test_add_new_voters(self):
        data = {'voting_id': 2, 'voters': [1,2,3,4], 'type': 'V'}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(data.get('voters')), Census.objects.count() - 1)

    def test_destroy_voter(self):
        data = {'voters': [1], 'type':'V'}
        response = self.client.delete('/census/{}/'.format(1), data, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(0, Census.objects.count())
