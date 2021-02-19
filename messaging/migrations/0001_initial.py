# Generated by Django 3.1.6 on 2021-02-19 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=70)),
                ('msgbody', models.CharField(max_length=700)),
                ('convoID', models.CharField(max_length=30)),
                ('send_time', models.DateTimeField(auto_now_add=True)),
                ('read_status', models.BooleanField(default=False)),
                ('sender_loc', models.CharField(max_length=30)),
                ('reciever_loc', models.CharField(max_length=30)),
                ('perm_del', models.BooleanField(default=False)),
            ],
        ),
    ]
