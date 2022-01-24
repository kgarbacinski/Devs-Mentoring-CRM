from django.apps import AppConfig


class ExercisesCheckerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Exercises_checker'

    def ready(self):
        import Exercises_checker.signals