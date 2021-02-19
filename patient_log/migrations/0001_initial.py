# Generated by Django 3.1.6 on 2021-02-19 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users_acc', '0002_auto_20210216_0334'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calories', models.IntegerField(default=0)),
                ('water', models.DecimalField(decimal_places=2, max_digits=5)),
                ('blood', models.DecimalField(decimal_places=2, max_digits=5)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient', to='users_acc.patient')),
            ],
        ),
    ]
