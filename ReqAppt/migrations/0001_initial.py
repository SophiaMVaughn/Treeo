# Generated by Django 3.1.6 on 2021-03-05 02:55

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
                ('meeturl', models.URLField(null=True)),
            ],
        ),
    ]
