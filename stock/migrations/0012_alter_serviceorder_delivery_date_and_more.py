# Generated by Django 5.1 on 2024-09-03 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0011_rename_deleviry_date_serviceorder_delivery_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceorder',
            name='delivery_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='serviceorder',
            name='delivery_forecast',
            field=models.DateField(null=True),
        ),
    ]
