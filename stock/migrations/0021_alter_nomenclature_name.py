from django.db import migrations, models, connection

def disable_triggers(apps, schema_editor):
    # Desativa triggers na tabela 'stock_nomenclature'
    with connection.cursor() as cursor:
        cursor.execute('ALTER TABLE stock_nomenclature DISABLE TRIGGER ALL;')

def enable_triggers(apps, schema_editor):
    # Reativa triggers na tabela 'stock_nomenclature'
    with connection.cursor() as cursor:
        cursor.execute('ALTER TABLE stock_nomenclature ENABLE TRIGGER ALL;')

def remove_duplicates(apps, schema_editor):
    # Obtenha o modelo Nomenclature
    Nomenclature = apps.get_model('stock', 'Nomenclature')

    # Encontrar registros duplicados com base no campo 'name'
    duplicates = Nomenclature.objects.values('name').annotate(name_count=models.Count('id')).filter(name_count__gt=1)

    # Para cada valor duplicado, mantém o primeiro registro e remove os restantes
    for duplicate in duplicates:
        duplicate_records = Nomenclature.objects.filter(name=duplicate['name']).order_by('id')[1:]
        for record in duplicate_records:
            record.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0020_remove_item_nomenclature'),
    ]

    operations = [
        # Desativa os triggers antes de qualquer modificação
        migrations.RunPython(disable_triggers),
        # Remove duplicatas antes de alterar o campo
        migrations.RunPython(remove_duplicates),
        # Altera o campo 'name' para ser único
        migrations.AlterField(
            model_name='nomenclature',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        # Reativa os triggers após as alterações
        migrations.RunPython(enable_triggers),
    ]