# Generated by Django 4.1.5 on 2023-03-09 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja_app', '0032_remove_produto_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='slug',
            field=models.SlugField(default='', unique=True),
        ),
    ]