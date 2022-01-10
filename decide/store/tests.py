import datetime
import random
from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from .models import Vote
from .serializers import VoteSerializer
from base import mods
from base.models import Auth
from base.tests import BaseTestCase
from census.models import Census
from mixnet.models import Key
from voting.models import Question
from voting.models import Voting


class StoreTextCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.question = Question(desc='qwerty')
        self.question.save()
        self.voting = Voting(id = 5001,name='voting example',
                             question=self.question,
                             start_date=timezone.now(),
                             type='V'
        )
        self.voting.save()

    def tearDown(self):
        super().tearDown()

    def gen_voting(self, id, type):
        voting = Voting(id=id, name='v1', question=self.question, start_date=timezone.now(),
                end_date=timezone.now() + datetime.timedelta(days=1), type=type)

        voting.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def gen_votes(self, type):
        votings = [random.randint(1, 5000) for i in range(10)]
        users = [random.randint(3, 5002) for i in range(50)]
        for v in votings:
            a = random.randint(2, 500)
            b = random.randint(2, 500)
            self.gen_voting(v, type)
            random_user = random.choice(users)
            user = self.get_or_create_user(random_user)
            self.login(user=user.username)
            census = Census(voting_id=v, voter_id=random_user, type=type)
            census.save()
            data = {
                "voting": v,
                "voter": random_user,
                "vote": { "a": a, "b": b },
                "type": type
            }
            response = self.client.post('/store/', data, format='json')
            self.assertEqual(response.status_code, 200)

        self.logout()
        return votings, users

    def test_gen_vote_invalid(self):
        data = {
            "voting": 5042,
            "voter": 1,
            "vote": { "a": 1, "b": 1 },
            "type": 'V'
        }
        response = self.client.post('/store/', data, format='json')
        self.assertEqual(response.status_code, 404)

    def test_store_vote(self):
        VOTING_PK = 345
        CTE_A = 96
        CTE_B = 184
        type='V'
        census = Census(voting_id=VOTING_PK, voter_id=1, type=type)
        census.save()
        self.gen_voting(VOTING_PK,type)
        data = {
            "voting": VOTING_PK,
            "voter": 1,
            "vote": { "a": CTE_A, "b": CTE_B },
            "type": type
        }
        user = self.get_or_create_user(1)
        self.login(user=user.username)
        response = self.client.post('/store/', data, format='json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(Vote.objects.first().voting_id, VOTING_PK)
        self.assertEqual(Vote.objects.first().voter_id, 1)
        self.assertEqual(Vote.objects.first().a, CTE_A)
        self.assertEqual(Vote.objects.first().b, CTE_B)
        self.assertEqual(Vote.objects.first().type, type)

    def test_vote(self):
        type='V'
        self.gen_votes(type)
        response = self.client.get('/store/', format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.get('/store/', format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get('/store/', format='json')
        self.assertEqual(response.status_code, 200)
        votes = response.json()

        self.assertEqual(len(votes), Vote.objects.count())
        self.assertEqual(votes[0], VoteSerializer(Vote.objects.all().first()).data)

    def test_filter(self):
        type='V'
        votings, voters = self.gen_votes(type)
        v = votings[0]

        response = self.client.get('/store/?voting_id={}&type={}'.format(v,type), format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.get('/store/?voting_id={}&type={}'.format(v,type), format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get('/store/?voting_id={}&type={}'.format(v,type), format='json')
        self.assertEqual(response.status_code, 200)
        votes = response.json()

        self.assertEqual(len(votes), Vote.objects.filter(voting_id=v, type=type).count())

        v = voters[0]
        response = self.client.get('/store/?voter_id={}&type={}'.format(v,type), format='json')
        self.assertEqual(response.status_code, 200)
        votes = response.json()

        self.assertEqual(len(votes), Vote.objects.filter(voter_id=v, type=type).count())

    def test_hasvote(self):
        type='V'
        votings, voters = self.gen_votes(type)
        vo = Vote.objects.first()
        v = vo.voting_id
        u = vo.voter_id
        type=vo.type

        response = self.client.get('/store/?voting_id={}&voter_id={}&type={}'.format(v, u, type), format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.get('/store/?voting_id={}&voter_id={}&type={}'.format(v, u, type), format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get('/store/?voting_id={}&voter_id={}&type={}'.format(v, u, type), format='json')
        self.assertEqual(response.status_code, 200)
        votes = response.json()

        self.assertEqual(len(votes), 1)
        self.assertEqual(votes[0]["voting_id"], v)
        self.assertEqual(votes[0]["voter_id"], u)
        self.assertEqual(votes[0]["type"], type)

    def test_voting_status(self):
        type = 'V'
        data = {
            "voting": 5001,
            "voter": 1,
            "vote": { "a": 30, "b": 55 },
            "type": type
        }
        census = Census(voting_id=5001, voter_id=1, type=type)
        census.save()
        # not opened
        self.voting.start_date = timezone.now() + datetime.timedelta(days=1)
        self.voting.save()
        user = self.get_or_create_user(1)
        self.login(user=user.username)
        response = self.client.post('/store/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # not closed
        self.voting.start_date = timezone.now() - datetime.timedelta(days=1)
        self.voting.save()
        self.voting.end_date = timezone.now() + datetime.timedelta(days=1)
        self.voting.save()
        response = self.client.post('/store/', data, format='json')
        self.assertEqual(response.status_code, 200)

        # closed
        self.voting.end_date = timezone.now() - datetime.timedelta(days=1)
        self.voting.save()
        response = self.client.post('/store/', data, format='json')
        self.assertEqual(response.status_code, 401)
    
    def test_voto_actualizado(self):
        VOTING_ID = 1234
        USUARIO = 69
        TYPE = 'V'

        #Creamos el usuario
        user = self.get_or_create_user(USUARIO)

        #Creamos la votación
        voting = self.gen_voting(VOTING_ID, TYPE)

        #Añadimos el usuario al censo
        census = Census(voting_id = VOTING_ID, voter_id = USUARIO, type = TYPE)
        census.save()

        #Votamos
        a1 = random.randint(50, 300)
        b1 = random.randint(50, 300)
        vote = Vote(voting_id = VOTING_ID, voter_id = USUARIO, a = a1, b = b1, type = TYPE)
        vote.save()
        self.login()
        response = self.client.get('/store/?voting_id={}&voter_id={}&type={}'.format(VOTING_ID, USUARIO, TYPE), format='json')
        self.assertEqual(response.status_code, 200)

        #Borramos el voto actual
        voto_registrado = Vote.objects.filter(voting_id=VOTING_ID, voter_id=USUARIO, type=TYPE)
        voto_registrado.delete()

        #Votamos de nuevo
        a2 = a1
        b2 = b1
        vote = Vote(voting_id = VOTING_ID, voter_id = USUARIO, a = a2, b = b2, type = TYPE)
        vote.save()
        
        response = self.client.get('/store/?voting_id={}&voter_id={}&type={}'.format(VOTING_ID, USUARIO, TYPE), format='json')
        self.assertEqual(response.status_code, 200)

        #Comprobamos que el voto se ha guardado correctamente, siendo solo un voto
        
        response = self.client.get('/store/?voting_id={}&voter_id={}&type={}'.format(VOTING_ID, USUARIO, TYPE), format='json')
        self.assertEqual(response.status_code, 200)
        votes = response.json()

        self.assertEqual(len(votes), 1)
        self.assertEqual(votes[0]["voting_id"], VOTING_ID)
        self.assertEqual(votes[0]["voter_id"], USUARIO)
        self.assertEqual(votes[0]["type"], TYPE)


    def test_voto_actualizado_error_votacion_cerrada(self):
        VOTING_ID = 1267
        USUARIO = 90
        TYPE = 'V'

        #Creamos el usuario
        user = self.get_or_create_user(USUARIO)

        #Creamos la votación
        voting = self.gen_voting(VOTING_ID, TYPE)

        #Añadimos el usuario al censo
        census = Census(voting_id = VOTING_ID, voter_id = USUARIO, type = TYPE)
        census.save()

        #Votamos
        a1 = random.randint(50, 300)
        b1 = random.randint(50, 300)
        vote = Vote(voting_id = VOTING_ID, voter_id = USUARIO, a = a1, b = b1, type = TYPE)
        vote.save()
        self.login()
        response = self.client.get('/store/?voting_id={}&voter_id={}&type={}'.format(VOTING_ID, USUARIO, TYPE), format='json')
        self.assertEqual(response.status_code, 200)

        #Borramos el voto actual
        voto_registrado = Vote.objects.filter(voting_id=VOTING_ID, voter_id=USUARIO, type=TYPE)
        voto_registrado.delete()

        #Cerramos la votación
        self.voting.end_date = timezone.now() - datetime.timedelta(days=1)
        self.voting.save()

        #Intentamos votar de nuevo y da error
        a2 = random.randint(50, 300)
        b2 = random.randint(50, 300)
        vote = {
            "voting_id": VOTING_ID,
            "voter_id": USUARIO,
            "a": a2,
            "b": b2,
            "type": TYPE
        }
        self.login(user=user.username)
        response = self.client.post('/store/', vote, format='json')
        self.assertEqual(response.status_code, 400)

