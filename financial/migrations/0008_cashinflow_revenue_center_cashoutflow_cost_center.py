# Generated by Django 5.1 on 2024-09-11 11:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0007_costcenter_revenuecenter'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashinflow',
            name='revenue_center',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='revenue_center_cashinflow', to='financial.revenuecenter'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cashoutflow',
            name='cost_center',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='cost_cente_cashoutflow', to='financial.costcenter'),
            preserve_default=False,
        ),
    ]
