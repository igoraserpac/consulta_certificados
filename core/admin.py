from django.contrib import admin
from .models import *
from rangefilter.filters import DateRangeFilter



@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email']
    search_fields = ['nome']
    ordering = ['nome']


@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'emissao', 'validade']
    fields = [
        'cliente',
        'ticket',
        'produto',
        'emissao',
        'validade',
        'valor',
        'observacao',
    ]
    autocomplete_fields = ['cliente', ]
    search_fields = ['cliente__nome']
    list_filter = [
        ('validade', DateRangeFilter),
        ('emissao', DateRangeFilter)
    ]
    ordering = ['-emissao']




