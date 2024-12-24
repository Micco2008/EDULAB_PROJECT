from rest_framework import serializers
from .models import Subject, Exam, Question, Answer


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['answer', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['question', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        question = Question.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)
        return question


class ExamSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Exam
        fields = ['name', 'subject', 'class_school', 'questions']

    def create(self, validated_data):
        subject_data = validated_data.pop('subject')
        questions_data = validated_data.pop('questions')

        subject_instance = Subject.objects.get(name=subject_data['name'])

        user = self.context['request'].user

        exam = Exam.objects.create(user=user, subject=subject_instance, **validated_data)

        for question_data in questions_data:
            question_serializer = QuestionSerializer(data=question_data)
            if question_serializer.is_valid():
                question_serializer.save(exam=exam)

        return exam