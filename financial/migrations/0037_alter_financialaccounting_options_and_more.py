# Generated by Django 5.1 on 2024-10-11 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0036_alter_chartofaccounts_category_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='financialaccounting',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='financialsubcategory',
            options={'ordering': ['id']},
        ),
    ]
