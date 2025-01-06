from django.db import models
from django.contrib.auth.models import User

class LogSistema(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Usuário")
    acao = models.CharField(max_length=255, verbose_name="Ação Realizada")
    detalhes = models.JSONField(blank=True, null=True, verbose_name="Detalhes")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Log do Sistema"
        verbose_name_plural = "Logs do Sistema"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.usuario} - {self.acao} - {self.criado_em}"


class Documento(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome do Documento")
    arquivo = models.FileField(upload_to="documentos/", verbose_name="Arquivo")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering = ["-criado_em"]

    def __str__(self):
        return self.nome
