# Generated by Django 3.2.7 on 2022-01-18 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='user_image',
            field=models.ImageField(blank=True, default='user_images/user.png', null=True, upload_to='user_images/'),
        ),
        migrations.AlterField(
            model_name='student',
            name='user_image',
            field=models.ImageField(blank=True, default='user_images/user.png', null=True, upload_to='user_images/'),
        ),
    ]