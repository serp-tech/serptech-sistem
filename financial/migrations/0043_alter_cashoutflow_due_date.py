# Generated by Django 5.1 on 2024-10-25 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0042_alter_cashoutflow_chart_of_accounts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashoutflow',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
