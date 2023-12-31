# Generated by Django 3.2.16 on 2023-04-26 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0042_rename_incident_id_prediction_ml_severity_incident_incident'),
    ]

    operations = [
        migrations.CreateModel(
            name='Engineer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('engineer_nickname', models.CharField(max_length=100, verbose_name='Nick Name')),
                ('company', models.ManyToManyField(blank=True, null=True, to='app.Company', verbose_name='Company of Engineer')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
