# Generated by Django 3.1 on 2021-05-27 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='manager',
            field=models.ManyToManyField(blank=True, null=True, to='app.Manager'),
        ),
    ]
