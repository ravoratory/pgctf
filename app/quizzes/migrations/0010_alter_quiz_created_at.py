# Generated by Django 3.2.4 on 2021-06-15 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0009_auto_20210615_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='created_at',
            field=models.DateTimeField(editable=False, verbose_name='Created at'),
        ),
    ]
