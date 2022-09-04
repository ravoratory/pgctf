import requests
import json
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Announcement
from quizzes.models import Quiz, Solved
from users.models import User


webhook_system_notify_url = settings.DISCORD_WEBHOOK_SYSTEM_NOTIFY_URL
webhook_solved_notify_url = settings.DISCORD_WEBHOOK_SOLVED_NOTIFY_URL


def discord_webhook_sender(payload, webhook_url):
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)

    return response


@receiver(post_save, sender=Quiz)
def quiz_create_receiver(sender, instance, created, **kwargs):
    if not created:
        return

    payload = {
        "content": ":question: New quiz created!",
        "embeds": [{
            "fields": [{
                "name": f"{instance.quiz_number}: [{instance.category.category_name}]",
                "value": instance.title,
            }]
        }],
    }
    discord_webhook_sender(payload, webhook_system_notify_url)

    if instance.published:
        Announcement.objects.create(title="問題公開", body=f"{instance.quiz_number}を公開しました")


@receiver(post_save, sender=Solved)
def quiz_solved_receiver(sender, instance, created, **kwargs):
    if not created:
        return

    payload = {
        "content": f":partying_face: {instance.user.username} solved {instance.quiz.quiz_number}: {instance.quiz.title}"
    }
    discord_webhook_sender(payload, webhook_solved_notify_url)


@receiver(post_save, sender=Announcement)
def announcement_create_receiver(sender, instance, created, **kwargs):
    if not created:
        return

    payload = {
        "content": ":microphone: New announcement created!",
        "embeds": [{
            "fields": [{
                "name": instance.title,
                "value": instance.body,
            }]
        }],
    }
    discord_webhook_sender(payload, webhook_system_notify_url)


@receiver(post_save, sender=User)
def user_register_receiver(sender, instance, created, **kwargs):
    if not created:
        return

    payload = {
        "content": f":tada: @{instance.username} has been registered!"
    }
    discord_webhook_sender(payload, webhook_system_notify_url)
