# Generated by Django 4.1.5 on 2023-03-21 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja_app', '0041_alter_ordempedido_pagamento_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordempedido',
            name='pagamento_method',
            field=models.CharField(choices=[('Pix', 'Pix'), ('Stripe', 'Stripe')], default='Pix', max_length=20),
        ),
    ]
