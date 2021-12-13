from django.db import models
from base.models import BigBigField


class Vote(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    a = BigBigField()
    b = BigBigField()

    voted = models.DateTimeField(auto_now=True)
    
    votingTypes = (('V', 'Voting'), ('BV', 'BinaryVoting'), ('MV', 'MultipleVoting'), ('SV', 'ScoreVoting'))
    type = models.CharField(max_length=2, choices=votingTypes)

    def __str__(self):
        return '{}: {}'.format(self.voting_id, self.voter_id)
