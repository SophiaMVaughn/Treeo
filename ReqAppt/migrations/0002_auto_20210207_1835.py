# Generated by Django 3.1.6 on 2021-02-07 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReqAppt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appttable',
            name='apptId',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
