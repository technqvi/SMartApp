# Generated by Django 3.2.16 on 2023-06-15 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_engineer'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='is_team_lead',
            field=models.BooleanField(default=False, verbose_name='Is Team Lead'),
        ),
        migrations.AddField(
            model_name='preventivemaintenance',
            name='engineer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='operation_engineer', to='app.employee', verbose_name='Engineer '),
        ),
        migrations.AlterField(
            model_name='preventivemaintenance',
            name='team_lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_lead_engineer', to='app.employee', verbose_name='Team Lead'),
        ),
    ]
