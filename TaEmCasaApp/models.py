from django.db import models

class Negocio(models.Model):
    nome = models.CharField(null=False)
    email = models.EmailField(null=False)
    tipo = models.CharField(null=False)
    estado = models.CharField(null=False)
    cidade = models.CharField(null=False)
    rua = models.CharField(null=False)
    numero = models.CharField(null=False)
    telefone_wpp = models.CharField(null=False)
    instagram_or_website = models.CharField(null=False)
    descricao = models.TextField(null=False)
    como_conheceu = models.TextField(null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    permitido = models.BooleanField(default=False)