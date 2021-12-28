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
            option.option = option_data.get("option",option.option)
            option.save()
        return instance