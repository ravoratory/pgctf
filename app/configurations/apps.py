from django.apps import AppConfig
from django.db.models.signals import post_migrate


class ConfigurationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "configurations"

    def ready(self):
        from .models import create_default_configuration

        post_migrate.connect(create_default_configuration, sender=self)
