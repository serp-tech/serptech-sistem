from django.db import migrations, models, transaction

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
        # Agrupa tudo em uma transação atômica para garantir que pendências sejam resolvidas
        migrations.RunPython(remove_duplicates),
        migrations.AlterField(
            model_name='nomenclature',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]

    @transaction.atomic  # Use o atomic para garantir que as operações sejam agrupadas em uma transação
    def apply(self, project_state, schema_editor, collect_sql=False):
        super().apply(project_state, schema_editor, collect_sql)