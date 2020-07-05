import datetime
import json

from bootstrap_modal_forms.mixins import PassRequestMixin
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from django.contrib.auth.models import User, Group
from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.shortcuts import redirect

from apps.recepcion.forms import LoginUserForm
from apps.recepcion.forms import CreateUserForm, UsuarioEmpresaForm
from apps.recepcion.forms import EditUserForm
from apps.recepcion.forms import EditPasswordForm
from apps.recepcion.forms import CreateSolicitanteForm
from apps.recepcion.forms import CreateEmpresaForm
from apps.recepcion.forms import CreateTipoPruebaForm
from apps.recepcion.forms import CrearAgendaForm, ActualizarAgendaForm
from apps.recepcion.forms import CrearResultadoForm
from apps.recepcion.forms import CreateEvaluadorForm
from apps.recepcion.forms import CrearFichaForm, UpdateFichaForm

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth import update_session_auth_hash

from django.views.generic import View, CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages  # Mensajes con funciones
from django.contrib.messages.views import SuccessMessageMixin  # mensajes con clases

from apps.recepcion.models import Persona, Empresa, TipoPrueba, Agenda, TipoResultado, Evaluador,Ficha
from facturacion.views import Precio


"""
Class
"""


class ShowClass(DetailView):
    model = User
    template_name = 'recepcion/show.html'
    slug_field = 'username'  # campo en la base de datos
    slug_url_kwarg = 'username_url'  # que de la url


class LoginClass(View):
    form = LoginUserForm()
    message = None
    template = 'recepcion/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('recepcion:dashboard')

        return render(request, self.template, self.get_context())

    def post(self, request, *args, **kwargs):
        username_post = request.POST['username']
        password_post = request.POST['password']
        user = authenticate(username=username_post, password=password_post)
        if user is not None:
            login_django(request, user)
            return redirect('recepcion:dashboard')
        else:
            self.message = "Username o password incorrectos"
        return render(request, self.template, self.get_context())

    def get_context(self):
        return {'form': self.form, 'message': self.message}


class DashboardClass(LoginRequiredMixin, View):
    login_url = 'recepcion:login'

    def get(self, request, *args, **kwargs):
        return render(request, 'recepcion/dashboard.html')


class EditClass(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    login_url = 'recepcion:login'
    model = User
    template_name = 'recepcion/edit.html'
    success_url = reverse_lazy('recepcion:edit')
    form_class = EditUserForm
    success_message = "Tu usuario ha sido actualizado"

    def form_valid(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EditClass, self).form_valid(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user


"""
Functions
"""


@login_required(login_url='recepcion:login')
def edit_password(request):
    form = EditPasswordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            current_password = form.cleaned_data['password']
            new_password = form.cleaned_data['new_password']
            if authenticate(username=request.user.username, password=current_password):
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'El password ha sido actualizado')
            else:
                messages.error(request, 'No es posible actualizar')

    context = {'form': form}
    return render(request, 'recepcion/edit_password.html', context)


def logout(request):
    logout_django(request)
    return redirect('home')


# CRUD DE SOLICITANTES---------------------------------------------------------------------------------------------------
class SolicitantesList(ListView):
    model = Persona
    template_name = 'recepcion/Solicitante/Solicitante.html'
    paginate_by = 5


class SolicitantesCreate(CreateView):
    success_url = reverse_lazy('recepcion:solicitante')
    template_name = 'recepcion/Solicitante/CrearSolicitanteForm.html'
    model = Persona
    form_class = CreateSolicitanteForm


class SolicitanteUpdate(UpdateView):
    model = Persona
    form_class = CreateSolicitanteForm
    template_name = 'recepcion/Solicitante/CrearSolicitanteForm.html'
    success_url = reverse_lazy('recepcion:solicitante')


class SolicitanteDelete(DeleteView):
    model = Persona
    template_name = 'recepcion/Solicitante/DeleteSolicitante.html'
    success_url = reverse_lazy('recepcion:solicitante')


# CRUD Usuario ----------------------------------------------------------------------------------------------------------
class CreateClass(CreateView):
    success_url = reverse_lazy('recepcion:dashboard')
    template_name = 'recepcion/Usuario/create.html'
    model = User
    form_class = CreateUserForm

    def form_valid(self, form):  # para que encripte la contra
        self.object = form.save(commit=False)  # crea el objeto pero no lo almacena(puede usarse para el ap)
        self.object.set_password(self.object.password)  # encripta el password
        self.object.save()  # guarda el objeto

        grupoEmpresas = Group.objects.get(name="Interno")
        grupoEmpresas.user_set.add(self.object)

        return HttpResponseRedirect(self.get_success_url())  # regresa la url definida en success:url


# Usuario de empresa------------------------------------------------------------------------------------------------------
class CreateUserEmpresa(CreateView):
    success_url = reverse_lazy('recepcion:dashboard')
    template_name = 'recepcion/Usuario/createUsuarioEmpresa.html'
    model = User
    form_class = UsuarioEmpresaForm

    def form_valid(self, form):  # para que encripte la contra
        self.object = form.save(commit=False)  # crea el objeto pero no lo almacena(puede usarse para el ap)
        self.object.set_password(self.object.password)  # encripta el password
        self.object.save()  # guarda el objeto
        grupoEmpresas = Group.objects.get(name="Empresas")
        grupoEmpresas.user_set.add(self.object)

        return HttpResponseRedirect(self.get_success_url())  # regresa la url definida en success:url


class UsuarioList(ListView):
    model = User
    template_name = 'recepcion/Usuario/Usuario.html'
    paginate_by = 10


class UsuarioUpdate(UpdateView):
    model = User
    form_class = CreateUserForm
    template_name = 'recepcion/Usuario/create.html'
    success_url = reverse_lazy('recepcion:usuario')


class UsuarioDelete(DeleteView):
    model = User
    template_name = 'recepcion/Usuario/UsuarioDelete.html'
    success_url = reverse_lazy('recepcion:usuario')


# CRUD Empresa ----------------------------------------------------------------------------------------------------------
class EmpresaCreate(CreateView):
    success_url = reverse_lazy('recepcion:empresas')
    template_name = 'recepcion/Empresa/EmpresaCreate.html'
    model = Empresa
    form_class = CreateEmpresaForm


class EmpresaList(ListView):
    model = Empresa
    template_name = 'recepcion/Empresa/Empresas.html'
    paginate_by = 10


class EmpresaUpdate(UpdateView):
    model = Empresa
    form_class = CreateEmpresaForm
    template_name = 'recepcion/Empresa/EmpresaCreate.html'
    success_url = reverse_lazy('recepcion:empresas')


class EmpresaDelete(DeleteView):
    model = Empresa
    template_name = 'recepcion/Empresa/EmpresaDelete.html'
    success_url = reverse_lazy('recepcion:empresas')


# CRUD TipoPrueba--------------------------------------------------------------------------------------------------------
class TipoPruebaCreate(CreateView):
    success_url = reverse_lazy('recepcion:pruebas')
    template_name = 'recepcion/TipoPrueba/TipoPruebaCreate.html'
    model = TipoPrueba
    form_class = CreateTipoPruebaForm


class TipoPruebaList(ListView):
    model = TipoPrueba
    template_name = 'recepcion/TipoPrueba/TiposPrueba.html'
    paginate_by = 10


class TipoPruebaUpdate(UpdateView):
    model = TipoPrueba
    form_class = CreateTipoPruebaForm
    template_name = 'recepcion/TipoPrueba/TipoPruebaCreate.html'
    success_url = reverse_lazy('recepcion:pruebas')


class TipoPruebaDelete(DeleteView):
    model = TipoPrueba
    template_name = 'recepcion/TipoPrueba/TipoPruebaDelete.html'
    success_url = reverse_lazy('recepcion:pruebas')


# CRUD Agenda -----------------------------------------------------------------------------------------------------------
class AgendaCreate(CreateView):
    success_url = reverse_lazy('recepcion:agendados')
    template_name = 'recepcion/Agenda/CreateAgenda.html'
    model = Agenda
    form_class = CrearAgendaForm


class AgendaList(ListView):
    model = Agenda
    template_name = 'recepcion/Agenda/Agendados.html'

    def get_queryset(self):
        return Agenda.objects.filter(fechaEvaluar=datetime.date.today())

    def get_context_data(self, **kwargs):
        context = super(AgendaList, self).get_context_data(**kwargs)
        ficha = Ficha.objects.all()

        context['ext'] = ficha
        return context


class BusquedaAjaxView(TemplateView):
    def get(self, request, *args, **kwargs):
        id_empresa = request.GET['id']
        personas = Persona.objects.filter(idEmpresa=id_empresa)
        personas = [ficha_serializer2(persona) for persona in personas]  # lista de diccionarios
        return HttpResponse(json.dumps(personas), content_type='application/json')


def ficha_serializer2(ficha):
    return {'idPersona': ficha.idPersona, 'nombre': ficha.nombre, 'apellidos': ficha.apellidos}


class AgendaUpdate(UpdateView):
    model = Agenda
    form_class = ActualizarAgendaForm
    template_name = 'recepcion/Agenda/CreateAgenda.html'
    success_url = reverse_lazy('recepcion:agendados')


# CRUD Tipo Resultado ---------------------------------------------------------------------------------------------------
class TipoResultadoCreate(CreateView):
    success_url = reverse_lazy('recepcion:resultados')
    template_name = 'recepcion/Resultado/ResultadoCreate.html'
    model = TipoResultado
    form_class = CrearResultadoForm


class TipoResultadoList(ListView):
    model = TipoResultado
    template_name = 'recepcion/Resultado/Resultados.html'
    paginate_by = 5


class TipoResultadoUpdate(UpdateView):
    model = TipoResultado
    form_class = CrearResultadoForm
    template_name = 'recepcion/Resultado/ResultadoCreate.html'
    success_url = reverse_lazy('recepcion:resultados')


class TipoResultadoDelete(DeleteView):
    model = TipoResultado
    template_name = 'recepcion/Resultado/ResultadoDelete.html'
    success_url = reverse_lazy('recepcion:resultados')


# CRUD Evaluador-------------------------------------------------------------------------------------------------------
class EvaluadorCreate(CreateView):
    success_url = reverse_lazy('recepcion:evaluadores')
    template_name = 'recepcion/Evaluador/EvaluadorCreate.html'
    model = Evaluador
    form_class = CreateEvaluadorForm


class EvaluadorList(ListView):
    model = Evaluador
    template_name = 'recepcion/Evaluador/Evaluadores.html'
    paginate_by = 10


class EvaluadorUpdate(UpdateView):
    model = Evaluador
    form_class = CreateEvaluadorForm
    template_name = 'recepcion/Evaluador/EvaluadorCreate.html'
    success_url = reverse_lazy('recepcion:evaluadores')


class EvaluadorDelete(DeleteView):
    model = Evaluador
    template_name = 'recepcion/Evaluador/EvaluadorDelete.html'
    success_url = reverse_lazy('recepcion:evaluadores')


# Buscador --------------------------------------------------------------------------------------------------------------
class BuscarView(TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            buscarx = request.POST['buscalo']
            dia = datetime.datetime.strptime(buscarx, '%d-%m-%Y')
            agenda = Agenda.objects.filter(fechaEvaluar=dia)
            return render(request, 'recepcion/Agenda/buscar.html', {'agendas': agenda, 'dia': buscarx})
        except:
            return redirect('recepcion:agendados')


# Ficha------------------------------------------------------------------------------------------------------------------
def FichaCreate(request, idagendado):
    agenda = Agenda.objects.get(idAgendado=idagendado)
    lst = 0
    form_ficha = CrearFichaForm(request.POST or None)
    if request.method == 'POST':
        if form_ficha.is_valid():
            form_ficha.save()
            messages.success(request, 'Ficha almacenada.')
            return redirect('recepcion:agendados')
    try:
        lst = Ficha.objects.latest('idFicha')
        op = lst.idFicha
    except:
        id = 1

    try:
        price = Precio.objects.get(idEmpresa=agenda.idEmpresa, idTipoPrueba=agenda.idTipoPrueba)
        valor = price.precio
    except:
        valor = 0

    id = op + 1
    print(id)

    context = {
        'id': id,
        'price': valor,
        'agenda': agenda,
        'form_ficha': form_ficha,
    }
    return render(request, 'recepcion/Ficha/FichaCreate.html', context)


def FichaFile(request):
    return render(request, 'recepcion/Ficha/FichaFile.html')


def search(request):
    fecha = request.GET.get('fecha')
    dui = request.GET.get('dui')
    ap = request.GET.get('ap')

    if not fecha:
        fichas = Ficha.objects.filter(Q(dui=dui) | Q(ap=ap))
        fichas = [ficha_serializer(ficha) for ficha in fichas]  # lista de diccionarios
        return HttpResponse(json.dumps(fichas), content_type='application/json')
    elif fecha and not dui and not ap:
        dia = datetime.datetime.strptime(fecha, '%d-%m-%Y')
        fichas = Ficha.objects.filter(Q(fechaFicha=dia) | Q(dui=dui))
        fichas = [ficha_serializer(ficha) for ficha in fichas]  # lista de diccionarios
        return HttpResponse(json.dumps(fichas), content_type='application/json')
    else:
        dia = datetime.datetime.strptime(fecha, '%d-%m-%Y')
        fichas = Ficha.objects.filter(Q(fechaFicha=dia) | Q(dui=dui) | Q(ap=ap))
        fichas = [ficha_serializer(ficha) for ficha in fichas]  # lista de diccionarios
        return HttpResponse(json.dumps(fichas), content_type='application/json')


def ficha_serializer(ficha):
    return {'Solicitante': ficha.idProgramado.idSolicitante.nombre, 'Empresa': ficha.idProgramado.idEmpresa.nombre,
            'AP': ficha.ap, 'Evaluado': ficha.idProgramado.nombreEvaluado, 'Resultado': ficha.idResultado.resultado}


class archivo(ListView):
    model = Ficha
    template_name = 'recepcion/Ficha/FichaList.html'

    def get_queryset(self):
        return Ficha.objects.filter(idResultado__resultado="indefinido")


class Archivar(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Ficha
    template_name = 'recepcion/Ficha/FichaUpdate.html'
    form_class = UpdateFichaForm
    success_message = 'Success: ficha was updated.'
    success_url = reverse_lazy('recepcion:archivos')


class FichaAgenda(UpdateView):
    model = Agenda
    second_model = Ficha
    template_name = 'recepcion/Agenda/FichaAgendados.html'
    form_class = CrearAgendaForm
    second_form_class = CrearFichaForm
    success_url = reverse_lazy('recepcion:agendados')

    def get_context_data(self, **kwargs):
        context = super(FichaAgenda, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        agenda = self.model.objects.get(idAgendado=pk)
        ficha = self.second_model.objects.get(idProgramado=agenda.idAgendado)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=ficha)
        context['id'] = ficha.idFicha
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        id_agenda = kwargs['pk']
        agenda = self.model.objects.get(idAgendado=id_agenda)
        ficha = self.second_model.objects.get(idProgramado=agenda.idAgendado)
        form = self.form_class(request.POST, instance=agenda)
        form2 = self.second_form_class(request.POST, instance=ficha)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(reverse_lazy('recepcion:dashboard'))


class UsuarioEmpresa(CreateView):
    model = User
    template_name = 'recepcion/Usuario/createUsuarioEmpresa.html'
    form_class = CreateUserForm
    second_form_class = UsuarioEmpresaForm
    success_url = reverse_lazy('recepcion:usuario')

    def get_context_data(self, **kwargs):
        context = super(UsuarioEmpresa, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(usuario.password)
            usuario = form.save()
            profile = form2.save(commit=False)
            profile.user = usuario
            profile.save()

            grupoEmpresas = Group.objects.get(name="Empresas")
            grupoEmpresas.user_set.add(usuario)

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))



