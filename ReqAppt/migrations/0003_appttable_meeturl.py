# Generated by Django 3.1.6 on 2021-02-21 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReqAppt', '0002_auto_20210220_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='appttable',
            name='meeturl',
            field=models.URLField(null=True),
        ),
    ]