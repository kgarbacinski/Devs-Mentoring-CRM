from django.db import models


class Exercise(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.name}"

class ExerciseTest(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    input = models.TextField()
    output = models.BooleanField()

    def __str__(self):
        return f'{self.exercise.name}'