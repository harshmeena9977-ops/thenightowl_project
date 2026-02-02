from django.apps import AppConfig

class NightowlmainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nightowlmainapp'

    def ready(self):
        import nightowlmainapp.signals