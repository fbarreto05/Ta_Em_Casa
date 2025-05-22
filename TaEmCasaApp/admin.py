from django.contrib import admin
from .models import Negocio

@admin.register(Negocio)
class negocioAdmin(admin.ModelAdmin):
    list_display = ('email', 'cidade')

