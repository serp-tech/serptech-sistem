# Generated by Django 5.1 on 2024-09-17 14:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0016_alter_costcenter_final_area_delete_finalarea'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinalArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='costcenter',
            name='final_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='costcenter_final', to='financial.finalarea'),
        ),
    ]