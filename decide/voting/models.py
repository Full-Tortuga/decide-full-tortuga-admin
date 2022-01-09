from django.db.models.signals import post_save
from django.dispatch import receiver
from base import mods
from mixnet.models import Mixnet
from store.models import Vote
from djongo import models
from django.core.exceptions import ValidationError


from base.models import Auth, Key


class ScoreQuestion(models.Model):
    desc = models.TextField()

    def __str__(self):
        return self.desc

class ScoreQuestionOption(models.Model):
    question = models.ForeignKey(ScoreQuestion, related_name='options', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(blank=True, null=True)
    option = models.PositiveIntegerField()

    def save(self):
        if not self.number:
            self.number = self.question.options.count() + 2
        return super().save()

    def __str__(self):
        return '{} ({})'.format(self.option, self.number)

class ScoreVoting(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    question = models.ForeignKey(ScoreQuestion, related_name='scorevoting', on_delete=models.CASCADE)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    pub_key = models.OneToOneField(Key, related_name='scorevoting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='scorevoting')

    tally = models.Field(blank=True, null=True, default=[])
    postproc = models.Field(blank=True, null=True, default=[])

    uniqueType = (('SV', 'ScoreVoting'),)
    type = models.CharField(max_length=2, choices= uniqueType,default='SV')

    def toJson(self):
        json = {'id': self.id, 
                'name': self.name, 
                'desc': self.desc, 
                'start_date': str(self.start_date),
                'end_date': str(self.end_date),
                'auths': [{'name': self.auths.all()[0].name, 
                            'url': self.auths.all()[0].url, 
                            'me': self.auths.all()[0].me}], 
                'tally': self.tally, 
                'postproc': self.postproc,
                'type':self.type}
        question = {'desc': self.question.desc}
        options = []
        for o in self.question.options.all():
            options.append({'number': o.number,'option':o.option})
        question['options'] = options
        json['question'] = question

        if self.pub_key == None:
            json['pub_key'] = 'None'
        else:
            json['pub_key'] = {'p': str(self.pub_key.p), 
                            'g': str(self.pub_key.g), 
                            'y': str(self.pub_key.y)}

        return json

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [ {"name": a.name, "url": a.url} for a in self.auths.all() ],
            "type": self.type
        }
        key = mods.post('mixnet', baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=''):
        votes = Vote.objects.filter(voting_id=self.pk,type=self.type).all()

        return [[i.a, i.b] for i in votes]

    def tally_votes(self, token=''):
        '''
        The tally is a shuffle and then a decrypt
        '''

        votes = self.get_votes(token)

        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        data = { "msgs": votes,
                "type": self.type }
        response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        if response.status_code != 200:
            pass

        data = {"msgs": response.json(),
                "type": self.type}
        response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)

        if response.status_code != 200:
            pass

        self.tally = response.json()
        self.save()

        self.do_postproc()

    def do_postproc(self):
        tally = self.tally
        options = self.question.options.all()

        opts = []
        for opt in options:
            if isinstance(tally, list):
                votes = tally.count(opt.number)
            else:
                votes = 0
            opts.append({
                'option': opt.option,
                'number': opt.number,
                'votes': votes
            })

        data = { 'type': 'IDENTITY', 'options': opts }
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save()

    def __str__(self):
        return self.name


class BinaryQuestion(models.Model):
    desc = models.TextField()

    def __str__(self):
        return self.desc

class BinaryQuestionOption(models.Model):
    question = models.ForeignKey(BinaryQuestion, related_name='options', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(blank=True, null=True)
    option = models.BooleanField(choices=[(1,('De acuerdo')),(0,('En desacuerdo'))])

    def save(self):
        if not self.number:
            self.number = self.question.options.count() + 2
        return super().save()

    def __str__(self):
        return '{} ({})'.format(self.option, self.number)

class BinaryVoting(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    question = models.ForeignKey(BinaryQuestion, related_name='binaryvoting', on_delete=models.CASCADE)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    pub_key = models.OneToOneField(Key, related_name='binaryvoting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='binaryvoting')

    tally = models.Field(blank=True, null=True, default=[])
    postproc = models.Field(blank=True, null=True, default=[])

    uniqueType = (('BV', 'BinaryVoting'),)
    type = models.CharField(max_length=2, choices= uniqueType,default='BV')

    def toJson(self):
        json = {'id': self.id, 
                'name': self.name, 
                'desc': self.desc, 
                'start_date': str(self.start_date),
                'end_date': str(self.end_date),
                'auths': [{'name': self.auths.all()[0].name, 
                            'url': self.auths.all()[0].url, 
                            'me': self.auths.all()[0].me}], 
                'tally': self.tally, 
                'postproc': self.postproc,
                'type':self.type}
        question = {'desc': self.question.desc}
        options = []
        for o in self.question.options.all():
            options.append({'number': o.number,'option':o.option})
        question['options'] = options
        json['question'] = question

        if self.pub_key == None:
            json['pub_key'] = 'None'
        else:
            json['pub_key'] = {'p': str(self.pub_key.p), 
                            'g': str(self.pub_key.g), 
                            'y': str(self.pub_key.y)}

        return json

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [ {"name": a.name, "url": a.url} for a in self.auths.all() ],
            "type": self.type
        }
        key = mods.post('mixnet', baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=''):
        votes = Vote.objects.filter(voting_id=self.pk,type=self.type).all()

        return [[i.a, i.b] for i in votes]

    def tally_votes(self, token=''):
        '''
        The tally is a shuffle and then a decrypt
        '''

        votes = self.get_votes(token)

        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        data = { "msgs": votes,
                "type": self.type }

        response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        if response.status_code != 200:
            pass

        data = {"msgs": response.json(),
                "type": self.type}

        response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)

        if response.status_code != 200:
            pass

        self.tally = response.json()
        self.save()

        self.do_postproc()

    def do_postproc(self):
        tally = self.tally
        options = self.question.options.all()

        opts = []
        for opt in options:
            if isinstance(tally, list):
                votes = tally.count(opt.number)
            else:
                votes = 0
            opts.append({
                'option': opt.option,
                'number': opt.number,
                'votes': votes
            })

        data = { 'type': 'IDENTITY', 'options': opts }
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save()

    def __str__(self):
        return self.name

class Question(models.Model):
    desc = models.TextField()

    def __str__(self):
        return self.desc


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(blank=True, null=True)
    option = models.TextField()

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.question.options.count() + 2
        return super().save()

    def __str__(self):
        return '{} ({})'.format(self.option, self.number)


class Voting(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    question = models.ForeignKey(Question, related_name='voting', on_delete=models.CASCADE, primary_key=False, db_index=False)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
        
    pub_key = models.ForeignKey(Key, related_name='voting', on_delete=models.CASCADE, null=True, blank=True, db_index=False)
    auths = models.ManyToManyField(Auth, related_name='votings')

    tally = models.Field(blank=True, null=True, default=[])
    postproc = models.Field(blank=True, null=True, default=[])

    uniqueType = (('V', 'Voting'),)
    type = models.CharField(max_length=2, choices= uniqueType,default='V')

    def toJson(self):
        json = {'id': self.id, 
                'name': self.name, 
                'desc': self.desc, 
                'start_date': str(self.start_date),
                'end_date': str(self.end_date),
                'auths': [{'name': self.auths.all()[0].name, 
                            'url': self.auths.all()[0].url, 
                            'me': self.auths.all()[0].me}], 
                'tally': self.tally, 
                'postproc': self.postproc,
                'type':self.type}
        question = {'desc': self.question.desc}
        options = []
        for o in self.question.options.all():
            options.append({'number': o.number,'option':o.option})
        question['options'] = options
        json['question'] = question

        if self.pub_key == None:
            json['pub_key'] = 'None'
        else:
            json['pub_key'] = {'p': str(self.pub_key.p), 
                            'g': str(self.pub_key.g), 
                            'y': str(self.pub_key.y)}

        return json

    def clean(self):
        
        if (self.pub_key is not None) and (Voting.objects.filter(pub_key=self.pub_key).exists()):
            raise ValidationError('There is already exists this public key', code='Error') 

    def create_pubkey(self):

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [ {"name": a.name, "url": a.url} for a in self.auths.all() ],
            "type": self.type
        }
        key = mods.post('mixnet', baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk

        self.save()

    def get_votes(self, token=''):
        
        votes = Vote.objects.filter(voting_id=self.pk,type=self.type).all()
       
        return [[i.a, i.b] for i in votes]

    def tally_votes(self, token=''):
        '''
        The tally is a shuffle and then a decrypt

        '''
        votes = self.get_votes(token)
        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]
        
      
        data = { "msgs": votes,
                "type": self.type }
        response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        if response.status_code != 200:
            
            pass
        
        
        data = {"msgs": response.json(),
                "type": self.type }
        response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)

        if response.status_code != 200:
            
            pass    
        
        self.tally = response.json()
        
        self.save()
        self.do_postproc()

    def do_postproc(self):
        tally = self.tally
        options = self.question.options.all()

        opts = []
        for opt in options:
            if isinstance(tally, list):
                votes = tally.count(opt.number)
            else:
                votes = 0
            opts.append({
                'option': opt.option,
                'number': opt.number,
                'votes': votes
            })

        data = { 'type': 'IDENTITY', 'options': opts }
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save()

    def __str__(self):
        return self.name

class MultipleQuestion(models.Model):
    desc = models.TextField()

    def __str__(self):
        return self.desc

class MultipleQuestionOption(models.Model):
    question = models.ForeignKey(MultipleQuestion, related_name='options', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(blank=True, null=True)
    option = models.TextField()

    def save(self):
        if not self.number:
            self.number = self.question.options.count() + 2
        return super().save()

    def __str__(self):
        return '{} ({})'.format(self.option, self.number)


class MultipleVoting(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    question = models.ForeignKey(MultipleQuestion, related_name='multiplevoting', on_delete=models.CASCADE)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    pub_key = models.OneToOneField(Key, related_name='multiplevoting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='multiplevoting')

    tally = models.Field(blank=True, null=True, default=[])
    postproc = models.Field(blank=True, null=True, default=[])

    uniqueType = (('MV', 'MultipleVoting'),)
    type = models.CharField(max_length=2, choices= uniqueType,default='MV')

    def toJson(self):
        json = {'id': self.id, 
                'name': self.name, 
                'desc': self.desc, 
                'start_date': str(self.start_date),
                'end_date': str(self.end_date),
                'auths': [{'name': self.auths.all()[0].name, 
                            'url': self.auths.all()[0].url, 
                            'me': self.auths.all()[0].me}], 
                'tally': self.tally, 
                'postproc': self.postproc,
                'type':self.type}
        question = {'desc': self.question.desc}
        options = []
        for o in self.question.options.all():
            options.append({'number': o.number,'option':o.option})
        question['options'] = options
        json['question'] = question

        if self.pub_key == None:
            json['pub_key'] = 'None'
        else:
            json['pub_key'] = {'p': str(self.pub_key.p), 
                            'g': str(self.pub_key.g), 
                            'y': str(self.pub_key.y)}
        
        return json

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [ {"name": a.name, "url": a.url} for a in self.auths.all() ],
            "type": self.type
        }
        key = mods.post('mixnet', baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=''):
        votes = Vote.objects.filter(voting_id=self.pk,type=self.type).all()

        return [[i.a, i.b] for i in votes]

    def tally_votes(self, token=''):
        '''
        The tally is a shuffle and then a decrypt
        '''

        votes = self.get_votes(token)

        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        data = { "msgs": votes,
                "type": self.type }
        response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        if response.status_code != 200:
            pass

        data = {"msgs": response.json(),
                "type": self.type }
        response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)

        if response.status_code != 200:
            pass

        self.tally = response.json()
        self.save()

        self.do_postproc()

    def do_postproc(self):
        tally = self.tally
        options = self.question.options.all()

        opts = []
        for opt in options:
            if isinstance(tally, list):
                votes = tally.count(opt.number)
            else:
                votes = 0
            opts.append({
                'option': opt.option,
                'number': opt.number,
                'votes': votes
            })

        data = { 'type': 'IDENTITY', 'options': opts }
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save()

    def __str__(self):
        return self.name
