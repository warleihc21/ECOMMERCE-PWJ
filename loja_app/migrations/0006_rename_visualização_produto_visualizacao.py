# Generated by Django 4.1.6 on 2023-02-17 02:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loja_app', '0005_produto_preco_compra_alter_produto_preco_mercado_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produto',
            old_name='visualização',
            new_name='visualizacao',
        ),
    ]
