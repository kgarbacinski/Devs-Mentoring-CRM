# Generated by Django 3.2.7 on 2021-10-09 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Files_organizer', '0002_document_studentdocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgrammingPath',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='path_images')),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.RemoveField(
            model_name='studentdocument',
            name='material',
        ),
        migrations.RemoveField(
            model_name='studentdocument',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='studentdocument',
            name='user',
        ),
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.DeleteModel(
            name='StudentDocument',
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
    ]
