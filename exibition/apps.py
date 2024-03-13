from django.apps import AppConfig


class ExibitionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exibition'

    def ready(self):
        import exibition.signals
