# Generated by Django 3.2.7 on 2022-01-18 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_management', '0002_auto_20220118_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='user_image',
            field=models.ImageField(blank=True, default='user.png', null=True, upload_to='user_images/'),
        ),
        migrations.AlterField(
            model_name='student',
            name='user_image',
            field=models.ImageField(blank=True, default='user.png', null=True, upload_to='user_images/'),
        ),
    ]
