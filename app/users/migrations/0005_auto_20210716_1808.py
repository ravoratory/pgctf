# Generated by Django 3.2.5 on 2021-07-16 09:08

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_date_joined'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 16, 9, 8, 4, 691287, tzinfo=utc), editable=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='管理サイトにログインできるかを指定します。'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'このユーザー名は既に使用されています'}, help_text="ユーザー名は4~30文字の英数字と'_'が使用できます", max_length=30, unique=True, validators=[users.models.UsernameValidator(), django.core.validators.MinLengthValidator(4)], verbose_name='Username'),
        ),
    ]
