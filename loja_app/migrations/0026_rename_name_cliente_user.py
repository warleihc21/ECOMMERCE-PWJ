# Generated by Django 4.1.6 on 2023-02-24 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loja_app', '0025_rename_user_cliente_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cliente',
            old_name='name',
            new_name='user',
        ),
    ]