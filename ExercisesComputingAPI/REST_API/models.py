from django.db import models
from django.utils.text import slugify


class Language(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=40)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return f"{self.name}, {self.language.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class ExerciseTest(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    input = models.TextField()
    output = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.exercise.name}, {self.exercise.language.name}'



