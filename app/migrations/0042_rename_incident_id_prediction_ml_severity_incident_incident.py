# Generated by Django 3.2.16 on 2023-04-04 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0041_auto_20230404_1637'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prediction_ml_severity_incident',
            old_name='incident_id',
            new_name='incident',
        ),
    ]
