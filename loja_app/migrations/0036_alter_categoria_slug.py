# Generated by Django 4.1.5 on 2023-03-10 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja_app', '0035_alter_produto_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='slug',
            field=models.SlugField(),
        ),
    ]
