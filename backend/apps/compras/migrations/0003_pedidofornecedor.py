# Generated by Django 5.1.2 on 2025-01-06 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0002_fornecedor_delete_comprasmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='PedidoFornecedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=255, verbose_name='Descrição')),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor Total')),
                ('data_pedido', models.DateField(verbose_name='Data do Pedido')),
            ],
            options={
                'verbose_name': 'Pedido de Fornecedor',
                'verbose_name_plural': 'Pedidos de Fornecedores',
            },
        ),
    ]