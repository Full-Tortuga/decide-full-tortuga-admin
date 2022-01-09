from django.contrib.auth.models import User

from base.models import Auth
from census.models import Census
from voting.models import Question, QuestionOption, Voting
from rest_framework import serializers
from base.serializers import AuthSerializer


class UserAdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'email', 'is_active', 'is_staff', 'is_superuser')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class AdminQuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ('id', 'number', 'option')


class UserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, min_length=1)
    first_name = serializers.CharField(max_length=30, allow_blank=True)
    last_name = serializers.CharField(max_length=150, allow_blank=True)
    email = serializers.EmailField()


class AdminQuestionSerializer(serializers.ModelSerializer):
    options = AdminQuestionOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'desc', 'options')
        depth = 1

    def create(self, validated_data):
        options_data = validated_data.pop("options")
        question = Question.objects.create(**validated_data)
        for option_data in options_data:
            QuestionOption.objects.create(question=question, **option_data)
        return question

    def update(self, instance, validated_data):
        options_data = validated_data.pop("options")
        options = (instance.options).all()
        options = list(options)
        instance.desc = validated_data.get("desc", instance.desc)
        instance.save()
        for option_data in options_data:
            option = options.pop(0)
            option.number = option_data.get("number", option.number)
            option.option = option_data.get("option", option.option)
            option.save()
        return instance


class CensusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Census
        fields = ('id', 'voting_id', 'voter_id')


class AdminVotingSerializer(serializers.Serializer):
    question = AdminQuestionSerializer(many=False)
    auth = serializers.URLField()
    name = serializers.CharField(max_length=200)
    desc = serializers.CharField(
        max_length=1000, allow_blank=True, allow_null=True)
    census = serializers.ListField(allow_null=True)


class AdminVotingGetSerializer(serializers.HyperlinkedModelSerializer):
    question = AdminQuestionSerializer(many=False)
    census = serializers.SerializerMethodField()
    auth = serializers.SerializerMethodField()

    class Meta:
        model = Voting
        fields = ('id', 'name', 'desc', 'question', 'auth',
                  'census', "end_date", "start_date", "tally")

    def get_auth(self, obj):
        auth = obj.auths.all().first()
        if auth is not None:
            return auth.url
        else:
            return ''

    def get_census(self, obj):
        censuss = Census.objects.filter(voting_id=obj.id)
        return [census.voter_id for census in censuss]
