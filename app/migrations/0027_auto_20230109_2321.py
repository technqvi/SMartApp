# Generated by Django 3.2.16 on 2023-01-09 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_alter_preventivemaintenance_remark'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pm_inventory',
            name='engineer',
        ),
        migrations.RemoveField(
            model_name='project',
            name='required_pm',
        ),
        migrations.AddField(
            model_name='pm_inventory',
            name='call_number',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Call Number'),
        ),
        migrations.AddField(
            model_name='pm_inventory',
            name='document_engineer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='document_engineer', to='app.employee', verbose_name='Document Engineer'),
        ),
        migrations.AddField(
            model_name='pm_inventory',
            name='pm_document_number',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='PM Doc Number'),
        ),
        migrations.AddField(
            model_name='pm_inventory',
            name='pm_engineer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pm_engineer', to='app.employee', verbose_name='PM Engineer'),
        ),
        migrations.AlterField(
            model_name='project',
            name='customer_po',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='CustPO/ContractNo'),
        ),
    ]
