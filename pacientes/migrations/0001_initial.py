# Generated by Django 4.2.16 on 2024-10-18 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('rg', models.CharField(max_length=20, unique=True)),
                ('endereco', models.TextField()),
                ('telefone', models.CharField(max_length=20)),
                ('historico_medico', models.TextField()),
                ('plano_saude', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
