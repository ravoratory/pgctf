# Generated by Django 3.2.15 on 2022-09-04 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=100)),
                ('value', models.TextField()),
                ('description', models.TextField()),
            ],
        ),
    ]
