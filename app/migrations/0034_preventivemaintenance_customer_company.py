# Generated by Django 3.2.16 on 2023-02-27 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_subcompany'),
    ]

    operations = [
        migrations.AddField(
            model_name='preventivemaintenance',
            name='customer_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.subcompany', verbose_name='Customer Company'),
        ),
    ]
