# Generated by Django 4.1.6 on 2023-02-15 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja_app', '0003_alter_produto_imagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='imagem',
            field=models.ImageField(upload_to='produtos'),
        ),
    ]