# Generated by Django 4.1.6 on 2023-02-15 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja_app', '0002_carrinho_carrinhoproduto_categoria_cliente_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='imagem',
            field=models.ImageField(upload_to='produto'),
        ),
    ]