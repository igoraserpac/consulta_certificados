import datetime

from django import forms
from .models import *


class CertificadoForm(forms.ModelForm):
    class Meta:
        model = Certificado
        fields = [
            'cliente',
            'ticket',
            'produto',
            'emissao',
            'validade',
            'valor',
            'observacao',
        ]
        this_year = datetime.date.today().year
        widgets = {'emissao': forms.SelectDateWidget(years=range(this_year-20, this_year+10)),
                   'validade': forms.SelectDateWidget(years=range(this_year-20, this_year+10)),
                   'cliente': forms.Select()}


class TransferirCertificadoForm(forms.Form):
    origem = forms.ModelChoiceField(Cliente.objects.all())
    destino = forms.ModelChoiceField(Cliente.objects.all())
