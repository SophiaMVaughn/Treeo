# Generated by Django 3.1.6 on 2021-02-28 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users_acc', '0001_initial'),
        ('patient_log', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientlog',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users_acc.patient'),
        ),
    ]
