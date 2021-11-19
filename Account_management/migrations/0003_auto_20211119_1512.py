# Generated by Django 3.2.7 on 2021-11-19 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_management', '0002_paymentinfo_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='paymentinfo',
            name='vat',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
