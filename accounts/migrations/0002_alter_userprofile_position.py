# Generated by Django 5.1 on 2024-09-20 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='position',
            field=models.CharField(choices=[('Estagiário', 'Estagiário'), ('Auxiliar', 'Auxiliar'), ('Assistente', 'Assistente'), ('Contador', 'Contador'), ('Gerente', 'Gerente'), ('Diretor', 'Diretor')], max_length=50),
        ),
    ]