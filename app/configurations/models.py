import time

from django.conf import settings
from django.db import models
from django.db.models import BooleanField, FloatField
from django.db.models.functions import Cast


class Configuration(models.Model):
    field = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=100, default="0")
    description = models.TextField()

    def __str__(self):
        return f"{self.field}: {self.value}"

    @staticmethod
    def quiz_viewable() -> bool:
        return (
            Configuration.objects.filter(field="quiz_viewable")
            .annotate(viewable=Cast("value", output_field=BooleanField()))
            .first()
            .viewable
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
    def game_ongoing() -> bool:
        start_ts = (
            Configuration.objects.filter(field="start_ts")
            .annotate(timestamp=Cast("value", output_field=FloatField()))
            .first()
            .timestamp
        )
        end_ts = (
            Configuration.objects.filter(field="end_ts")
            .annotate(timestamp=Cast("value", output_field=FloatField()))
            .first()
            .timestamp
        )

        if start_ts is None:
            return False
        elif end_ts is None:
            return start_ts <= time.time()
        else:
            return start_ts <= time.time() < end_ts

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
    def ranking_viewable() -> bool:
        return (
            Configuration.objects.filter(field="ranking_viewable")
            .annotate(ranking_viewable=Cast("value", output_field=BooleanField()))
            .first()
            .ranking_viewable
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

    @staticmethod
    def max_score() -> int:
        return (
            Configuration.objects.filter(field="max_score")
            .annotate(max_score=Cast("value", output_field=models.IntegerField()))
            .first()
            .max_score
        )

    @staticmethod
    def min_score() -> int:
        return (
            Configuration.objects.filter(field="min_score")
            .annotate(min_score=Cast("value", output_field=models.IntegerField()))
            .first()
            .min_score
        )

    @staticmethod
    def winners_threshould() -> int:
        return (
            Configuration.objects.filter(field="winners_threshould")
            .annotate(winners_threshould=Cast("value", output_field=models.IntegerField()))
            .first()
            .winners_threshould
        )


def create_default_configuration(sender, **kwargs):
    for field, value, description in settings.DEFAULT_GAME_CONFIGURATIONS:
        try:
            Configuration.objects.get_or_create(field=field, value=value, description=description)
        except Exception:
            pass
