from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from Account_management.models import Mentor, Student


# Create your models here.
class Meeting(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.date.strftime("%d-%m-%Y, %H:%M")} - {self.mentor.__str__()}'


class Note(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name="notes", blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True, blank=True)
    text = models.TextField()

    # def validate_unique(self, *args, **kwargs):
    #     super(Note, self).validate_unique(*args, **kwargs)
    #
    #     if self.__class__.objects.filter(meeting=self.meeting, author=self.author).exists():
    #         raise ValidationError(
    #             message='MyModel with this (fk, my_field) already exists.',
    #             code='unique_together',
    #         )

    class Meta:
        unique_together = [['meeting', 'author']]

    def __str__(self):
        return self.text
