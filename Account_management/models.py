import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from dateutil import relativedelta
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime
from payments import PurchasedItem
from payments.models import BasePayment
from decouple import config


class Path(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to='user_images/', default='user.png', null=True, blank=True)
    max_students = models.IntegerField(default=1)

    def count_all_meetings(self):
        current_hour = datetime.now()
        return self.meeting_set.filter(date__lte=current_hour).count()

    def count_all_students(self):
        return self.student_set.count()

    def get_remaining_meetings(self):
        return 4 - self.count_all_meetings() % 4

    def save(self, *args, **kwargs):
        try:
            this = Mentor.objects.get(id=self.id)
            if this.user_image != self.user_image and self.user_image.name != 'user.png':
                this.user_image.delete(save=False)
        except:
            pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mentor = models.ManyToManyField(Mentor)
    enrollmentDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    path = models.ForeignKey(Path, on_delete=models.PROTECT)
    user_image = models.ImageField(upload_to='user_images/', default='user.png', null=True, blank=True)
    no_month = models.IntegerField(default=1)

    def get_next_payment(self):
        if list(self.payment_set.all()):
            return list(self.payment_set.all())[-1].next_payment
        return "not paid"

    def count_all_meetings(self):
        current_hour = datetime.now()
        return self.meeting_set.filter(date__lte=current_hour).count()

    def get_remaining_meetings(self):
        if self.is_sub_paid() is False:
            return 0
        return 4 - self.count_all_meetings() % 4

    def count_month_number(self):
        if self.count_all_meetings() % 4 == 0:
            self.no_month += 1

    def is_sub_paid(self):
        no_payments = self.payment_set.count()
        if self.no_month <= no_payments:
            return True
        return False

    def save(self, *args, **kwargs):
        try:
            this = Student.objects.get(id=self.id)
            if this.user_image != self.user_image and self.user_image.name != 'user.png':
                this.user_image.delete(save=False)
        except:
            pass
        super().save(*args, **kwargs)

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
    country = models.CharField(max_length=20, default='Poland')
    phone = PhoneNumberField()
    email = models.EmailField()
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.student.__str__()


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    paymentDate = models.DateField()
    is_paid = models.BooleanField(default=False)

    @property
    def next_payment(self):
        return self.paymentDate + relativedelta.relativedelta(months=1)


class CoursePayment(BasePayment):
    id = models.CharField(
        primary_key=True, editable=False, default=uuid.uuid4, max_length=50
    )

    # TODO change urls
    def get_failure_url(self):
        print(reverse('failure'))
        return f"{config('HOST')}{reverse('failure')}"  # "https://przelewy24.source.net.pl/fail"

    def get_success_url(self):
        print(reverse('success'))
        return f"{config('HOST')}{reverse('success')}"  # "https://przelewy24.source.net.pl/success"

    def get_purchased_items(self):
        # you'll probably want to retrieve these from an associated order
        yield PurchasedItem(
            name="The Hound of the Baskervilles",
            sku="BSKV",
            quantity=9,
            price=Decimal(10),
            currency="USD",
        )
