# Generated by Django 4.2.5 on 2023-11-19 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subEntrado', '0012_alter_appointment_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
