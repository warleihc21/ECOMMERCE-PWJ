# Generated by Django 4.1.5 on 2023-03-08 23:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loja_app', '0029_remove_produto_imagem_imagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='categoria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja_app.categoria'),
        ),
        migrations.DeleteModel(
            name='Imagem',
        ),
    ]
