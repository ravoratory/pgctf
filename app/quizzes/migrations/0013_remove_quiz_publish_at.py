# Generated by Django 3.2.15 on 2022-09-08 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0012_quiz_publish_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='publish_at',
        ),
    ]
