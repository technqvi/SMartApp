# Generated by Django 3.1 on 2022-04-25 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20220425_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_end',
            field=models.DateField(verbose_name='Project-End'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_start',
            field=models.DateField(verbose_name='Project-Start'),
        ),
    ]
