from os import read
from voting.models import Question, QuestionOption, Voting
from rest_framework import serializers

class AdminQuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ('id','number', 'option')

class AdminQuestionSerializer(serializers.ModelSerializer):
    opts = AdminQuestionOptionSerializer(many=True)
    class Meta:
        model = Question
        fields = ('id','desc', 'opts')

    def update(self, instance, validated_data):
        instance.desc = validated_data["desc"]
        instance.save()
        for item in validated_data["options"]:
            qOption = QuestionOption(number=item["number"], option=item["option"])
            qOption.save()
        return instance

class AdminQuestionSerializerGetPost(serializers.ModelSerializer):
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
 