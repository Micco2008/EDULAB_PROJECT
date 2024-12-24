from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField('Предмет', max_length=100)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.name


class Exam(models.Model):
    name = models.CharField('Имя', max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,
                                related_name='exams', verbose_name='Предмет')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    class_school = models.IntegerField('Класс',
        validators=[MinValueValidator(1), MaxValueValidator(11)]
    )

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.name


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE,
                             related_name='questions', verbose_name='тест')
    question = models.TextField('Вопрос')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.question


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='answers')
    answer = models.TextField()
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.answer

