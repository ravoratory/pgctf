# Generated by Django 3.2.5 on 2021-07-16 09:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210716_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 16, 9, 8, 6, 845520, tzinfo=utc), editable=False),
        ),
    ]