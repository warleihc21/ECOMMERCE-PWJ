# Generated by Django 4.1.6 on 2023-02-23 23:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loja_app', '0022_alter_cliente_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cliente',
            old_name='user',
            new_name='username',
        ),
    ]
