# Generated by Django 3.2.4 on 2021-06-15 09:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_date_started'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='アカウント作成日'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_started',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='CTF開始時間'),
        ),
    ]
