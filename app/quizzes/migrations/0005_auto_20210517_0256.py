# Generated by Django 3.2.2 on 2021-05-16 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0004_alter_quizcategory_category_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='category',
        ),
        migrations.AddField(
            model_name='quiz',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='quizzes.quizcategory'),
        ),
    ]
