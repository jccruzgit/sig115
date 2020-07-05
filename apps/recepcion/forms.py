from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django import forms
from django.contrib.auth.models import User

from apps.recepcion.models import Persona, Empresa, TipoPrueba, Agenda, TipoResultado, Evaluador, Ficha, Profile
from ArguetaServicios import settings

"""
Constants
"""
ERROR_MESSAGE_USER = {'required': 'El usuario es obligatorio', 'unique': 'El usuario ya se encuentra registrado',
                      'invalid': 'El username no es correo'}
ERROR_MESSAGE_PASSWORD = {'required': 'El password es obligatorio'}
ERROR_MESSAGE_EMAIL = {'required': 'El correo es obligatorio', 'invalid': 'El correo no es valido'}

"""
Funciones

"""


def must_be_gt(value_password):
    if len(value_password) < 5:
        raise forms.ValidationError('El password debe de tener al menos 5 caracteres')


"""
Class
"""


class LoginUserForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())
    username.label = 'Usuario:'
    password.label = 'contraseña'

    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'username_login'})
        self.fields['password'].widget.attrs.update({'class': 'username_login'})


class CreateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=20, error_messages=ERROR_MESSAGE_USER)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(), error_messages=ERROR_MESSAGE_PASSWORD)
    email = forms.CharField(error_messages=ERROR_MESSAGE_EMAIL)

    first_name = forms.CharField(max_length=25, error_messages={'required': 'El nombre es obligatorio'})
    last_name = forms.CharField(max_length=25, error_messages={'required': 'El apellido es obligatorio'})

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')


class EditUserForm(forms.ModelForm):
    username = forms.CharField(max_length=20, error_messages=ERROR_MESSAGE_USER)
    email = forms.CharField(error_messages=ERROR_MESSAGE_EMAIL)

    class Meta:
        model = User
        fields = {'username', 'email', 'first_name', 'last_name'}


class EditPasswordForm(forms.Form):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())
    new_password = forms.CharField(max_length=20, widget=forms.PasswordInput(), validators=[must_be_gt])
    repeat_password = forms.CharField(max_length=20, widget=forms.PasswordInput(), validators=[must_be_gt])

    def clean(self):
        clean_data = super(EditPasswordForm, self).clean()
        password1 = clean_data.get('new_password')
        password2 = clean_data.get('repeat_password')
        if password1 != password2:
            raise forms.ValidationError('Las password no son los mismos')


# FORM SOLICITANTE
class CreateSolicitanteForm(forms.ModelForm):
    class Meta:
        model = Persona
        exclude = ['idSolicitante']


# Form Empresa
class CreateEmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['codEmpresa', 'nit', 'nrc', 'nombre', 'direccion', 'giro']
        labels = {
            'nombre': 'Empresa nombre',
            'codEmpresa': 'Codigo Empresa',
            'direccion': 'Direccion',
            'giro': 'giro',
            'nit': 'Numero Identificacion Tributaria: xxxx-xxxxxx-xxx-x',
            'nrc': 'Numero de Registro de Contribuyente: xxxxxx-x',

        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input-field'}),
            'codEmpresa': forms.TextInput(attrs={'class': 'input-field'}),
            'direccion': forms.TextInput(attrs={'class': 'input-field'}),
            'giro': forms.TextInput(attrs={'class': 'input-field'}),
            'nit': forms.TextInput(
                attrs={'class': 'input-field', 'id': 'nit', 'pattern': '^[0-9]{4}-[0-9]{6}-[0-9]{3}-[0-9]{1}$',
                       'placeholder': 'xxxx-xxxxxx-xxx-x', 'data-inputmask': "'mask': '9999-999999-999-9'"}),
            'nrc': forms.TextInput(
                attrs={'class': 'input-field', 'id': 'nrc', 'pattern': '^[0-9]{6}-[0-9]{1}$', 'placeholder': 'xxxxxx-x',
                       'data-inputmask': "'mask': '999999-9'"}),
        }


class CreateTipoPruebaForm(forms.ModelForm):
    class Meta:
        model = TipoPrueba
        fields = ['tipoPrueba']
        labels = {
            'tipoPrueba': 'Tipo de prueba'
        }
        widgets = {
            'tipoPrueba': forms.TextInput(attrs={'class': 'input-field'}),
        }


class CrearAgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        exclude = ['idAgendado', 'asistencia']
        fechaEvaluar = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
        labels = {
            'idSolicitante': 'Solicitante',
            'idEmpresa': 'Empresa:',
            'idTipoPrueba': 'Tipo de prueba',
            'fechaEvaluar': 'Fecha ha evaluarse :',
            'nombreEvaluado': 'Nombre del evaluado:',
            'puesto': 'Puesto Solicitado :',
            'horaProgramada': 'Hora Programada:',
        }
        widgets = {
            'idSolicitante': forms.Select(attrs={'class': 'form-control', 'id': 'idSolicitante'}),
            'idEmpresa': forms.Select(attrs={'class': 'form-control', 'id': 'idEmpresa'}),
            'idTipoPrueba': forms.Select(attrs={'class': 'form-control', 'id': 'idTipoPrueba'}),
            'fechaEvaluar': forms.DateInput(format='%d-%m-%Y',
                                            attrs={'class': 'form-control', 'id': 'fecha', 'type': 'date'}),
            'nombreEvaluado': forms.TextInput(attrs={'class': 'form-control', 'id': 'nombreEvaluado'}),
            'puesto': forms.TextInput(attrs={'class': 'form-control', 'id': 'puesto'}),
            'horaProgramada': forms.TextInput(attrs={'class': 'form-control', 'id': 'hora', 'type': 'time'}),
        }


class ActualizarAgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        exclude = ['idAgendado']
        fechaEvaluar = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
        labels = {
            'idSolicitante': 'Solicitante',
            'idEmpresa': 'Empresa:',
            'idTipoPrueba': 'Tipo de prueba',
            'fechaEvaluar': 'Fecha ha evaluarse :',
            'nombreEvaluado': 'Nombre del evaluado:',
            'puesto': 'Puesto Solicitado :',
            'horaProgramada': 'Hora Programada:',
            'asistencia': 'Asistencia'
        }
        widgets = {
            'idSolicitante': forms.Select(attrs={'class': 'form-control', 'id': 'idSolicitante'}),
            'idEmpresa': forms.Select(attrs={'class': 'form-control', 'id': 'idEmpresa'}),
            'idTipoPrueba': forms.Select(attrs={'class': 'form-control', 'id': 'idTipoPrueba'}),
            'fechaEvaluar': forms.DateInput(attrs={'class': 'form-control', 'id': 'fecha', 'type': 'date'}),
            'nombreEvaluado': forms.TextInput(attrs={'class': 'form-control', 'id': 'nombreEvaluado'}),
            'puesto': forms.TextInput(attrs={'class': 'form-control', 'id': 'puesto'}),
            'horaProgramada': forms.TextInput(attrs={'class': 'form-control', 'id': 'hora', 'type': 'time'}),
            'asistencia': forms.CheckboxInput(attrs={'class': 'switch', 'id': 'asistencia'}),
        }


# Para Ficha
# ------------------------------------------------------------------------------------------------------------
class CrearFichaForm(forms.ModelForm):
    class Meta:
        model = Ficha
        exclude = ['idFicha', 'fechaFicha', 'facturado']
        labels = {
            'idEvaluador': 'Evaluador:',
            'idResultado': 'Resultado',
            'ap': 'AP :',
            'dui': 'Documento identidad:',
            'observaciones': 'Observaciones :',

        }
        widgets = {
            'idEvaluador': forms.Select(attrs={'class': 'input-field col s6', 'id': 'idevaluador'}),
            'idResultado': forms.Select(attrs={'class': 'input-field col s6'}),
            'idProgramado': forms.TextInput(attrs={'class': 'hide'}),
            'precio': forms.TextInput(attrs={'class': 'hide', 'id': 'precio'}),
            #  'idFicha': forms.TextInput(attrs={'class': 'hide'}),
            'ap': forms.TextInput(attrs={'class': 'input-field'}),
            'dui': forms.TextInput(attrs={'class': 'input-field ', 'data-inputmask': "'mask': '99999999-9'"}),
            'observaciones': forms.Textarea(attrs={'class': 'materialize-textarea'}),
        }


class UpdateFichaForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = Ficha
        exclude = ['idFicha', 'facturado', 'idProgramado', 'precio']
        labels = {

            'idEvaluador': 'Evaluador',
            'idResultado': 'Resultado',
            'ap': 'AP',
            'dui': 'Documento de identidad',
            'observaciones': 'Observaciones',
        }
        widgets = {
            'idEvaluador': forms.Select(attrs={'class': 'custom-select', 'id': 'idevaluador'}),
            'idResultado': forms.Select(attrs={'class': 'custom-select'}),
            # 'idProgramado': forms.TextInput(attrs={'class': 'invisible'}),
            #  'idFicha': forms.TextInput(attrs={'class': 'hide'}),
            'ap': forms.TextInput(attrs={'class': 'input-group-text'}),
            'dui': forms.TextInput(attrs={'class': 'input-group-text', 'data-inputmask': "'mask': '99999999-9'"}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
        }


# para resultado --------------------------------------------------------------------------------------------------------
class CrearResultadoForm(forms.ModelForm):
    class Meta:
        model = TipoResultado
        exclude = ['idTipoResultado']
        labels = {
            'resultado': 'Resultado:',
        }
        widgets = {
            'resultado': forms.TextInput(attrs={'class': 'input-field'}),
        }


# Form Evaluador
class CreateEvaluadorForm(forms.ModelForm):
    class Meta:
        model = Evaluador
        exclude = ['idEvaluador']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input-field'}),
            'letra': forms.TextInput(attrs={'class': 'input-field'}),
        }


class UsuarioEmpresaForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['id', 'user']