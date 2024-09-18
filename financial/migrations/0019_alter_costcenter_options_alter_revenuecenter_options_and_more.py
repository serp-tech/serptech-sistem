# Generated by Django 5.1 on 2024-09-17 18:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0018_alter_costcenter_final_area_delete_finalarea'),
        ('stock', '0013_request_delivery_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='costcenter',
            options={'ordering': ['id_center']},
        ),
        migrations.AlterModelOptions(
            name='revenuecenter',
            options={'ordering': ['id_center']},
        ),
        migrations.RemoveField(
            model_name='revenuecenter',
            name='name',
        ),
        migrations.AddField(
            model_name='revenuecenter',
            name='area',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='area_revenue', to='financial.area'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='revenuecenter',
            name='final_area',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='final_area_revenue', to='financial.area'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='revenuecenter',
            name='id_center',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='revenuecenter',
            name='sector',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sector_revenue', to='stock.sector'),
            preserve_default=False,
        ),
    ]
