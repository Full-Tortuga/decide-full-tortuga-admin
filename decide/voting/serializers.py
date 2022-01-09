from rest_framework import serializers

from .models import Question, BinaryQuestion, MultipleQuestion, ScoreQuestion
from .models import QuestionOption, BinaryQuestionOption, MultipleQuestionOption, ScoreQuestionOption
from .models import Voting, BinaryVoting, MultipleVoting, ScoreVoting
from base.serializers import KeySerializer, AuthSerializer


class QuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ('number', 'option')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    options = QuestionOptionSerializer(many=True)
    class Meta:
        model = Question
        fields = ('desc', 'options')


class VotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = Voting
        fields = ('id', 'name', 'desc', 'question', 'start_date',
                  'end_date', 'pub_key', 'auths', 'tally', 'postproc', 'type')


class SimpleVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)

    class Meta:
        model = Voting
        fields = ('name', 'desc', 'question', 'start_date', 'end_date', 'type')


class BinaryQuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BinaryQuestionOption
        fields = ('number', 'option')

class BinaryQuestionSerializer(serializers.HyperlinkedModelSerializer):
    options = BinaryQuestionOptionSerializer(many=True)
    class Meta:
        model = BinaryQuestion
        fields = ('desc', 'options')

class BinaryVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = BinaryQuestionSerializer(many=False)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = BinaryVoting
        fields = ('id', 'name', 'desc', 'question', 'start_date',
                  'end_date', 'pub_key', 'auths', 'tally', 'postproc', 'type')

class SimpleBinaryVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = BinaryQuestionSerializer(many=False)

    class Meta:
        model = BinaryVoting
        fields = ('name', 'desc', 'question', 'start_date', 'end_date', 'type')

class MultipleQuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MultipleQuestionOption
        fields = ('number', 'option')

class MultipleQuestionSerializer(serializers.HyperlinkedModelSerializer):
    options = MultipleQuestionOptionSerializer(many=True)
    class Meta:
        model = MultipleQuestion
        fields = ('desc', 'options')

class MultipleVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = MultipleQuestionSerializer(many=False)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = MultipleVoting
        fields = ('id', 'name', 'desc', 'question', 'start_date',
                  'end_date', 'pub_key', 'auths', 'tally', 'postproc', 'type')

class SimpleMultipleVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = MultipleQuestionSerializer(many=False)

    class Meta:
        model = MultipleVoting
        fields = ('name', 'desc', 'question', 'start_date', 'end_date', 'type')

class ScoreQuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScoreQuestionOption
        fields = ('number', 'option')

class ScoreQuestionSerializer(serializers.HyperlinkedModelSerializer):
    options = ScoreQuestionOptionSerializer(many=True)
    class Meta:
        model = ScoreQuestion
        fields = ('desc', 'options')

class ScoreVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = ScoreQuestionSerializer(many=False)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = ScoreVoting
        fields = ('id', 'name', 'desc', 'question', 'start_date',
                  'end_date', 'pub_key', 'auths', 'tally', 'postproc', 'type')

class SimpleScoreVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = ScoreQuestionSerializer(many=False)

    class Meta:
        model = ScoreVoting
        fields = ('name', 'desc', 'question', 'start_date', 'end_date', 'type')
