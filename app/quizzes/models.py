import os

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class FlagValidator(RegexValidator):
    regex = r'^pgctf\{[\w_]{1,}\}$'
    message = 'Invalid flag format'
    flags = 0


class QuizCategory(models.Model):
    category_name = models.CharField('quiz', max_length=30, unique=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Quiz categories'


class QuizFile(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True)
    file = models.FileField(upload_to='quiz_files/')
    uploaded_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    @property
    def filename(self):
        return os.path.basename(self.file.name)


class Quiz(models.Model):
    quiz_number = models.CharField('Quiz number', max_length=100, unique=True)

    title = models.CharField('Quiz Title', max_length=100, unique=True)
    statement = models.TextField('Quiz Statement', blank=True, null=True)
    category = models.ManyToManyField(QuizCategory, related_name='quiz')

    file = models.ManyToManyField(QuizFile, related_name='quiz', null=True)

    flag = models.CharField(
        'Flag',
        max_length=100,
        validators=[FlagValidator()],
        unique=True,
    )

    difficulty = models.IntegerField('Difficulty')
    point = models.IntegerField('Point')

    solved_users = models.ManyToManyField(
        'users.User',
        related_name='solved_quiz',
        through='Solved',
    )

    published = models.BooleanField('Published', default=True)

    created_at = models.DateTimeField('Created at', default=timezone.now)
    updated_at = models.DateTimeField('Updated at', default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Quizzes'


class Solved(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)

    solved_datetime = models.DateTimeField('Solved date', default=timezone.now)
    elapsed_time = models.TimeField('Elapsed time')

    class Meta:
        verbose_name = 'Solved user'
        verbose_name_plural = 'Solved users'
