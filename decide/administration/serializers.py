from rest_framework import serializers

from django.contrib.auth.models import User
from os import read
from voting.models import Question, QuestionOption, Voting
from rest_framework import serializers

class UserAdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')

class AdminQuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ('id','number', 'option')

class AdminQuestionSerializer(serializers.ModelSerializer):
    options = AdminQuestionOptionSerializer(many=True)
    class Meta:
        model = Question
        fields = ('id','desc', 'options')
        depht=1

    def create(self, validated_data):
        options_data = validated_data.pop("options")
        question = Question.objects.create(**validated_data)
        for options_data in options_data:
            QuestionOption.objects.create(question=question, **options_data)
        return question

