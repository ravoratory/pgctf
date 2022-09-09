from django.conf import settings
from django.db import models
from django.db.models import BooleanField
from django.db.models.functions import Cast


class Configuration(models.Model):
    field = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.field}: {self.value}"

    @staticmethod
    def game_ongoing() -> bool:
        return (
            Configuration.objects.filter(field="game")
            .annotate(ongoing=Cast("value", output_field=BooleanField()))
            .first()
            .ongoing
        )

    @staticmethod
    def game_paused() -> bool:
        return (
            Configuration.objects.filter(field="game_paused")
            .annotate(paused=Cast("value", output_field=BooleanField()))
            .first()
            .paused
        )

    @staticmethod
    def auto_announce() -> bool:
        return (
            Configuration.objects.filter(field="auto_announce")
            .annotate(auto_announce=Cast("value", output_field=BooleanField()))
            .first()
            .auto_announce
        )

    @staticmethod
    def scoring() -> bool:
        return (
            Configuration.objects.filter(field="scoring")
            .annotate(scoring=Cast("value", output_field=BooleanField()))
            .first()
            .scoring
        )

    @staticmethod
    def update_score() -> bool:
        return (
            Configuration.objects.filter(field="update_score")
            .annotate(update_score=Cast("value", output_field=BooleanField()))
            .first()
            .update_score
        )

    @staticmethod
    def enable_ranking() -> bool:
        return (
            Configuration.objects.filter(field="ranking")
            .annotate(ranking=Cast("value", output_field=BooleanField()))
            .first()
            .ranking
        )

    @staticmethod
    def open_ranking() -> bool:
        return (
            Configuration.objects.filter(field="open_ranking")
            .annotate(open_ranking=Cast("value", output_field=BooleanField()))
            .first()
            .open_ranking
        )

    @staticmethod
    def can_registration() -> bool:
        return (
            Configuration.objects.filter(field="registration")
            .annotate(registration=Cast("value", output_field=BooleanField()))
            .first()
            .registration
        )

    @staticmethod
    def can_login() -> bool:
        return (
            Configuration.objects.filter(field="login")
            .annotate(login=Cast("value", output_field=BooleanField()))
            .first()
            .login
        )


def create_default_configuration(sender, **kwargs):
    for field, *_ in settings.DEFAULT_GAME_CONFIGURATIONS:
        Configuration.objects.get_or_create(field=field)
