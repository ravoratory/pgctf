# Generated by Django 3.2.15 on 2022-09-08 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0013_remove_quiz_publish_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='is_extra',
            field=models.BooleanField(default=False, verbose_name='Is extra'),
        ),
    ]
