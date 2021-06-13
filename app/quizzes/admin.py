from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Quiz)
admin.site.register(models.QuizCategory)
admin.site.register(models.QuizFile)
admin.site.register(models.QuizAppendedUrl)
admin.site.register(models.Solved)
