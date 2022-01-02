import random
import itertools
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods
from base.tests import BaseTestCase
from census.models import Census
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption, ScoreVoting, ScoreQuestion, ScoreQuestionOption

from django.test import Client

# Create your tests here.
class VisualizerTestCase(BaseTestCase):
    

    def get_or_create_user(self,pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_simple_voting(self):
        #Create Voting
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(id=101,name='test voting', question=q)

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        self.login()  # set token
        v.tally_votes(self.token)

        #Create Voters
        for i in range(50):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

        #Store Votes 
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        for opt in v.question.options.all():
            for i in range(random.randint(0, 5)):
                a, b = self.encrypt_msg(opt.number, v)
                data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'vote': { 'a': a, 'b': b },
                    'type': 'V'
                }
                user = self.get_or_create_user(voter.voter_id)
                self.login(user=user.username)
                voter = voters.pop()
                mods.post('store', json=data)

    def create_scoring_voting(self):
        
        #Create Voting
        q = ScoreQuestion(desc='test question')
        q.save()
        for i in range(5):
            opt = ScoreQuestionOption(question=q, option='{}'.format(i+1))
            opt.save()
        v = ScoreVoting(id=101,name='test voting', question=q)

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        self.login()  # set token
        v.tally_votes(self.token)

        #Create Voters
        for i in range(50):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

        #Store Votes 
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        for opt in v.question.options.all():
            for i in range(random.randint(0, 5)):
                data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'vote': { str(i): i},
                    'type': 'SV'
                }
                user = self.get_or_create_user(voter.voter_id)
                self.login(user=user.username)
                voter = voters.pop()
                self.client.post('/store/', data, format='json')

    def setUp(self):
        super().setUp()
        self.create_simple_voting()
        self.create_scoring_voting()
        
        
    def tearDown(self):
        super().tearDown()

    def test_visualizer_voting(self):
        response = self.client.get('/visualizer/scoringVoting/{}/'.format(101))
        self.assertEqual(response.status_code,200)
        response = self.client.get('/visualizer/votes/scoryVoting/{}/'.format(101))
        self.assertEqual(response['content-type'],'text/csv')   

    def test_visualizer_voting(self):
        response = self.client.get('/visualizer/{}/'.format(101))
        self.assertEqual(response.status_code,200)
        response = self.client.get('/visualizer/votes/{}/'.format(101))
        self.assertEqual(response['content-type'],'text/csv')

  