# Generated by Django 3.2.7 on 2021-10-09 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Files_organizer', '0004_auto_20211009_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='programmingpath',
            name='about',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
