# Generated by Django 5.1 on 2024-08-31 00:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inflow',
            name='unit',
        ),
        migrations.AddField(
            model_name='item',
            name='outflow_frequency',
            field=models.CharField(choices=[('Efetuada', 'Efetuada'), ('Não efetuada', 'Não efetuada')], default='Irregular', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='presentation',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='presentation_item', to='stock.presentation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchase_manager', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='manager_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
