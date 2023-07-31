# Generated by Django 3.1 on 2022-06-21 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20220621_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='asset_code',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Asset Code'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='building',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Building'),
        ),
    ]
