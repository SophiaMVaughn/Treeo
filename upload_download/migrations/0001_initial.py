# Generated by Django 3.1.6 on 2021-03-06 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Uploaded_File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='uploaded_files')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
