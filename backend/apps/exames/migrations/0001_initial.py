# Generated by Django 4.2.16 on 2024-11-08 00:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('documentos', '0001_initial'),
        ('pacientes', '__first__'),
        ('profissionais', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('tipo_exame', models.CharField(max_length=100, verbose_name='Tipo de Exame')),
                ('data_solicitacao', models.DateField(default=django.utils.timezone.now, verbose_name='Data de Solicitação')),
                ('data_realizacao', models.DateField(blank=True, null=True, verbose_name='Data de Realização')),
                ('resultados', models.TextField(blank=True, null=True, verbose_name='Resultados do Exame')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('status', models.CharField(choices=[('Solicitado', 'Solicitado'), ('Realizado', 'Realizado'), ('Cancelado', 'Cancelado')], default='Solicitado', max_length=20)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('documento_resultado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exames_resultados', to='documentos.documentosmodel', verbose_name='Documento do Resultado')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exames', to='pacientes.paciente')),
                ('profissional_solicitante', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exames_solicitados_exame', to='profissionais.profissional', verbose_name='Profissional Solicitante')),
            ],
            options={
                'verbose_name': 'Exame',
                'verbose_name_plural': 'Exames',
                'ordering': ['-data_solicitacao'],
            },
        ),
    ]