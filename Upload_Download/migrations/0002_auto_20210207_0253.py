# Generated by Django 3.1.6 on 2021-02-07 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload_download', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploaded_file',
            old_name='usern',
            new_name='uploading_user',
        ),
    ]
