import json

import requests

from django.conf import settings
from django.core.signals import got_request_exception
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpRequest

from configurations.models import Configuration
from quizzes.models import Quiz, Solved
from users.models import User

from .models import Announcement

webhook_system_notify_url = settings.DISCORD_WEBHOOK_SYSTEM_NOTIFY_URL
webhook_solved_notify_url = settings.DISCORD_WEBHOOK_SOLVED_NOTIFY_URL
webhook_error_notify_url = settings.DISCORD_WEBHOOK_ERROR_NOTIFY_URL


def discord_webhook_sender(payload, webhook_url):
    headers = {"Content-Type": "application/json"}

    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)

    return response


# 新しいクイズが作成された際の通知
@receiver(post_save, sender=Quiz)
def quiz_create_receiver(sender, instance, created, **kwargs):
    if not created:
        return

    payload = {
        "content": ":question: New quiz created!",
        "embeds": [
            {
                "fields": [
                    {
                        "name": f"{instance.number}: [{instance.category.name}]",
                        "value": instance.title,
                    }
                ]
            }
        ],
    }
    discord_webhook_sender(payload, webhook_system_notify_url)

    if instance.published and Configuration.auto_announce():
        Announcement.objects.create(title="問題公開", body=f"{instance.number}を公開しました")


# クイズが解かれた際の通知
@receiver(post_save, sender=Solved)
def quiz_solved_receiver(sender, instance, created, **kwargs):
    if not created:
        return

    payload = {
        "content": f":partying_face: {instance.user.username} solved {instance.quiz.number}: {instance.quiz.title}"
    }
    discord_webhook_sender(payload, webhook_solved_notify_url)


# Announcementが作成された際の通知
@receiver(post_save, sender=Announcement)
def announcement_create_receiver(sender, instance, created, **kwargs):
    if not created:
        return

    payload = {
        "content": ":microphone: New announcement!",
        "embeds": [
            {
                "fields": [
                    {
                        "name": instance.title,
                        "value": instance.body,
                    }
                ]
            }
        ],
    }
    discord_webhook_sender(payload, webhook_system_notify_url)


# Userが登録された際の通知
@receiver(post_save, sender=User)
def user_register_receiver(sender, instance, created, **kwargs):
    if not created:
        return

    payload = {"content": f":tada: @{instance.username} has been registered!"}
    discord_webhook_sender(payload, webhook_system_notify_url)


# Viewで例外(Status code 5xx)が発生した際の通知
# なぜかExceptionが取得できないので、とりあえず例外が発生したことだけを通知する
@receiver(got_request_exception)
def got_request_exception_receiver(sender: None, request: HttpRequest, **kwargs):
    payload = {
        "content": ":warning: Exception occurred!",
        "embeds": [
            {
                "fields": [
                    {
                        "name": "Path",
                        "value": f"`{request.path}`",
                        "inline": True,
                    },
                    {
                        "name": "Method",
                        "value": f"{request.method}",
                        "inline": True,
                    },
                    {
                        "name": "User",
                        "value": f"{request.user}",
                        "inline": True,
                    },
                ]
            }
        ],
    }
    discord_webhook_sender(payload, webhook_system_notify_url)
