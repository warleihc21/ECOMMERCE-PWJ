# Generated by Django 4.1.6 on 2023-02-24 00:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loja_app', '0023_rename_user_cliente_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cliente',
            old_name='username',
            new_name='user',
        ),
    ]
