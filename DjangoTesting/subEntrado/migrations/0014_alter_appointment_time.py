# Generated by Django 4.2.5 on 2023-11-19 21:10

from django.db import migrations, models
import subEntrado.validators


class Migration(migrations.Migration):

    dependencies = [
        ('subEntrado', '0013_alter_appointment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.TimeField(blank=True, null=True, validators=[subEntrado.validators.validate_within_time_range]),
        ),
    ]