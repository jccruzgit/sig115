from django import forms


class FormularioContacto(forms.Form):
    correo = forms.EmailField()
    mensaje = forms.CharField()
