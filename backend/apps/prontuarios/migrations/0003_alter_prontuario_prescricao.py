# Generated by Django 5.1.2 on 2025-01-02 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prontuarios', '0002_anamnese'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prontuario',
            name='prescricao',
            field=models.TextField(),
        ),
    ]
