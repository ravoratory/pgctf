import os

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class FlagValidator(RegexValidator):
    regex = r"^pgctf\{[\w_]{1,}\}$"
    message = "Invalid flag format"
    flags = 0


class QuizCategory(models.Model):
    category_name = models.CharField("Category", max_length=30, unique=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Quiz categories"


class QuizFile(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True)
    file = models.FileField(upload_to="quiz_files/")
    uploaded_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.uploaded_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)


class QuizAppendedUrl(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=256)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title or self.url

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)


class Quiz(models.Model):
    quiz_number = models.CharField("Quiz number", max_length=100, unique=True)

    title = models.CharField("Quiz Title", max_length=100, unique=True)
    statement = models.TextField("Quiz Statement", blank=True, null=True)
    category = models.ForeignKey(QuizCategory, related_name="quiz", on_delete=models.SET_NULL, blank=True, null=True)

    file = models.ManyToManyField(QuizFile, related_name="quiz", blank=True)
    url = models.ManyToManyField(QuizAppendedUrl, related_name="quiz", blank=True)

    flag = models.CharField(
        "Flag",
        max_length=100,
        validators=[FlagValidator()],
        unique=True,
    )

    difficulty = models.IntegerField("Difficulty")
    point = models.IntegerField("Point")

    author = models.CharField("Author", max_length=100, blank=True, null=True)

    solved_users = models.ManyToManyField(
        "users.User",
        related_name="solved_quiz",
        through="Solved",
    )

    published = models.BooleanField("Published", default=True)

    created_at = models.DateTimeField("Created at", editable=False)
    updated_at = models.DateTimeField("Updated at", default=timezone.now)

    is_extra = models.BooleanField("Is extra", default=False)

    def __str__(self):
        return f"{self.quiz_number}: {self.title}"

    class Meta:
        verbose_name_plural = "Quizzes"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)


class Solved(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE)

    solved_datetime = models.DateTimeField("Solved date", editable=False)

    def __str__(self):
        return f"{self.quiz.quiz_number}: {self.user.username} [{self.solved_datetime}]"

    class Meta:
        verbose_name = "Solved user"
        verbose_name_plural = "Solved users"

    def save(self, *args, **kwargs):
        if not self.id:
            self.solved_datetime = timezone.now()
        return super().save(*args, **kwargs)
