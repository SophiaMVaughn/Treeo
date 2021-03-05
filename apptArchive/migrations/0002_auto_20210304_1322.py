# Generated by Django 3.1.6 on 2021-03-04 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users_acc', '0001_initial'),
        ('apptArchive', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apptarchive',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users_acc.patient'),
        ),
        migrations.AddField(
            model_name='apptarchive',
            name='provider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users_acc.provider'),
        ),
    ]
