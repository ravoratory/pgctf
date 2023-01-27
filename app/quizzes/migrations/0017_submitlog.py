# Generated by Django 3.2.15 on 2022-09-19 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizzes', '0016_auto_20220909_2251'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmitLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag', models.CharField(max_length=100, verbose_name='Flag')),
                ('created_at', models.DateTimeField(editable=False, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(verbose_name='Updated at')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.quiz')),
                ('solved', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quizzes.solved')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]