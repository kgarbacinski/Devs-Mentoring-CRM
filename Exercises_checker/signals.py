from django.db.models.signals import post_save
from django.dispatch import receiver
from Exercises_checker.models import Exercise, ExerciseStatus


@receiver(post_save, sender=Exercise)
def create_exercise_statuses(sender, instance, created, **kwargs):
    if created:
        language = instance.language
        users = language.user.all()
        for user in users:
            ExerciseStatus.objects.create(user=user, exercise=instance).save()