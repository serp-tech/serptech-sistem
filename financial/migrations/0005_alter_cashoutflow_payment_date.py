# Generated by Django 5.1 on 2024-09-04 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0004_alter_cashinflow_payment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashoutflow',
            name='payment_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
