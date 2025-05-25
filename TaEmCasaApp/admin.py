from django.contrib import admin
from .models import Negocio

@admin.register(Negocio)
class negocioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'estado', 'cidade', 'rua', 'numero', 'email', 'telefone_wpp', 'instagram_or_website', 'descricao', 'como_conheceu', 'latitude', 'longitude', 'permitido')
    list_editable = (['permitido'])
