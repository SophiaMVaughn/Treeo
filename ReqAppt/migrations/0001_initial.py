# Generated by Django 3.1.6 on 2021-02-17 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApptTable',
            fields=[
                ('apptId', models.AutoField(primary_key=True, serialize=False)),
                ('meetingDate', models.DateTimeField()),
                ('status', models.BooleanField(default=False)),
            ],
        ),
    ]
