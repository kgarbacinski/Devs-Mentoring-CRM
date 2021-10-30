from django.db import models
from django.contrib.auth.models import User
from dateutil import relativedelta
from phonenumber_field.modelfields import PhoneNumberField


class Path(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mentor = models.ManyToManyField(Mentor)
    enrollmentDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    path = models.ForeignKey(Path, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class PaymentInfo(models.Model):
    student = models.OneToOneField(Student, on_delete=models.PROTECT, primary_key=True)
    firstName = models.CharField(max_length=10)
    lastName = models.CharField(max_length=25)
    companyName = models.CharField(max_length=100, null=True, blank=True)
    nip = models.CharField(max_length=10, null=True, blank=True)
    street = models.CharField(max_length=200)
    postCode = models.CharField(max_length=6)
    town = models.CharField(max_length=20)
    phone = PhoneNumberField()
    email = models.EmailField()
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.student.__str__()


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    paymentDate = models.DateField()

    @property
    def next_payment(self):
        return self.paymentDate + relativedelta.relativedelta(months=1)
