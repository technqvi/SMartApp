# Generated by Django 3.1 on 2021-09-15 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20210915_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='incident_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.incident_type', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='incident',
            name='incident_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.incident_status', verbose_name='Status'),
        ),
    ]
