# Generated by Django 3.2.23 on 2024-02-02 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0056_incident_summary_userfeedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incident_summary_userfeedback',
            old_name='incident_summary_id',
            new_name='incident_summary',
        ),
        migrations.RenameField(
            model_name='incident_summary_userfeedback',
            old_name='user_id',
            new_name='user',
        ),
    ]