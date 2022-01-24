from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import m2m_changed


class Language(models.Model):
    name = models.CharField(max_length=40)
    user = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=40)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    class Type(models.TextChoices):
        EASY = 'EASY'
        MEDIUM = 'MEDIUM'
        HARD = "HARD"

    type = models.CharField(
        max_length=10,
        choices=Type.choices)

    def __str__(self):
        return f"{self.name, self.language.name}"


class ExerciseStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, null=True, on_delete=models.SET_NULL)
    done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}, {self.exercise.name}, Done: {self.done}"


def create_exercise_status(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add':
        exercises = Exercise.objects.filter(language=instance).all()
        for user_id in pk_set:
            for exercise in exercises:
                ExerciseStatus.objects.create(user_id=user_id, exercise_id=exercise.id).save()


m2m_changed.connect(create_exercise_status, sender=Language.user.through)
