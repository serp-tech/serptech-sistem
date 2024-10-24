from django.db import migrations, models


def remove_duplicates(apps, schema_editor):
    # Obtenha o modelo Nomenclature
    Nomenclature = apps.get_model('stock', 'Nomenclature')

    # Encontrar registros duplicados com base no campo 'name'
    duplicates = Nomenclature.objects.values('name').annotate(name_count=models.Count('id')).filter(name_count__gt=1)

    # Para cada valor duplicado, mantém o primeiro registro e remove os restantes
    for duplicate in duplicates:
        # Recupera todos os registros duplicados
        duplicate_records = Nomenclature.objects.filter(name=duplicate['name']).order_by('id')
        
        # Mantém o primeiro registro e exclui os outros
        for record in duplicate_records[1:]:
            record.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0020_remove_item_nomenclature'),
    ]

    operations = [
        # Adiciona o passo de remover duplicatas antes de alterar o campo para único
        migrations.RunPython(remove_duplicates),
        # Em seguida, aplica a alteração de campo para torná-lo único
        migrations.AlterField(
            model_name='nomenclature',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]