from django.apps import AppConfig


class ContestantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contestants'

    def ready(self):
        from contestants import signals
