from django import forms
from django.contrib.auth.models import User
from .models import Precio, Documentos
from ArguetaServicios import settings
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class CrearPrecioForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = Precio
        exclude = ['idPrecio']
        labels = {
            'idEmpresa': 'Empresa:',
            'idTipoPrueba': 'Tipo de prueba',
            'precio': 'Precio'
        }
        widgets = {
            'idEmpresa': forms.Select(attrs={'class': 'custom-select'}),
            'idTipoPrueba': forms.Select(attrs={'class': 'custom-select'}),
            'precio': forms.NumberInput(attrs={'class': 'input-field'}),
        }


class DocumentosForm(forms.ModelForm):
    class Meta:
        model = Documentos
        exclude = ['idDocumento']
        labels = {
            'nombre': 'Nombre',
            'documento': 'documento',
            'idEmpresa': 'Empresa'
        }

        widgets = {
            'idEmpresa': forms.Select(attrs={'class': 'custom-select'}),
            'nombre': forms.TextInput(attrs={'class': 'input-field'}),
            'docuemnto': forms.FileInput(),

        }
