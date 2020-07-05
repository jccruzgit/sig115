from django.conf.urls import url
from apps.recepcion.views import ShowClass
from apps.recepcion.views import LoginClass
from apps.recepcion.views import logout
from apps.recepcion.views import DashboardClass
from apps.recepcion.views import CreateClass
from apps.recepcion.views import EditClass
from apps.recepcion.views import edit_password
from apps.recepcion.views import SolicitantesList
from apps.recepcion.views import SolicitantesCreate
from apps.recepcion.views import SolicitanteUpdate
from apps.recepcion.views import SolicitanteDelete
from apps.recepcion.views import UsuarioList, UsuarioUpdate, UsuarioDelete, CreateUserEmpresa, UsuarioEmpresa
from apps.recepcion.views import EmpresaCreate, EmpresaList, EmpresaUpdate, EmpresaDelete
from apps.recepcion.views import TipoPruebaCreate, TipoPruebaDelete, TipoPruebaList, TipoPruebaUpdate
from apps.recepcion.views import TipoResultadoList, TipoResultadoCreate, TipoResultadoDelete, TipoResultadoUpdate
from apps.recepcion.views import AgendaCreate, AgendaList, AgendaUpdate, FichaAgenda
from apps.recepcion.views import EvaluadorCreate, EvaluadorList, EvaluadorUpdate, EvaluadorDelete
from apps.recepcion.views import BuscarView, BusquedaAjaxView
from apps.recepcion.views import FichaCreate, FichaFile, search, archivo, Archivar
from django.conf.urls import include

from django.contrib.auth.decorators import login_required

app_name = 'recepcion'

urlpatterns = [
    # url(r'^show/(?P<pk>\d+)/$', views.ShowView.as_view(), name='show'),
    url(r'^show/(?P<username_url>\w+)/$', login_required(ShowClass.as_view()), name='show'),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^login/$', LoginClass.as_view(), name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^dashboard/$', login_required(DashboardClass.as_view()), name='dashboard'),
    # Usuario
    url(r'^Usuario/$', login_required(UsuarioList.as_view()), name='usuario'),
    url(r'^create/$', login_required(CreateClass.as_view()), name='create'),
    url(r'^usuariocliente/$', login_required(UsuarioEmpresa.as_view()), name='cliente'),
    url(r'^Usuarioupdate/(?P<pk>\d+)/$', login_required(UsuarioUpdate.as_view()), name='userUpdate'),
    url(r'^Usuariodelete/(?P<pk>\d+)/$', login_required(UsuarioDelete.as_view()), name='userDelete'),
    url(r'^edit/$', login_required(EditClass.as_view()), name='edit'),
    # Solicitante
    url(r'^edit_password/$', login_required(edit_password), name='edit_password'),
    url(r'^Solicitantes/$', login_required(SolicitantesList.as_view()), name='solicitante'),
    url(r'^Solicitantes/add$', login_required(SolicitantesCreate.as_view()), name='solicitante/add'),
    url(r'^SolicitanteUpdate/(?P<pk>\d+)/$', login_required(SolicitanteUpdate.as_view()), name='solicitante/update'),
    url(r'^SolicitanteDelete/(?P<pk>\d+)/$', login_required(SolicitanteDelete.as_view()), name='solicitante/Delete'),
    # Empresa
    url(r'^Empresa/add/$', login_required(EmpresaCreate.as_view()), name='empresa'),
    url(r'^Empresas', login_required(EmpresaList.as_view()), name='empresas'),
    url(r'^Empresa/update/(?P<pk>\d+)/$', login_required(EmpresaUpdate.as_view()), name='empresaupdate'),
    url(r'^Empresa/Delete/(?P<pk>\d+)/$', login_required(EmpresaDelete.as_view()), name='empresadelete'),
    # TipoPrueba
    url(r'^tipoprueba/add/$', login_required(TipoPruebaCreate.as_view()), name='pruebaadd'),
    url(r'^tiposprueba', login_required(TipoPruebaList.as_view()), name='pruebas'),
    url(r'^tipoprueba/update/(?P<pk>\d+)/$', login_required(TipoPruebaUpdate.as_view()), name='pruebaupdate'),
    url(r'^tipoprueba/Delete/(?P<pk>\d+)/$', login_required(TipoPruebaDelete.as_view()), name='pruebadelete'),

    # TipoResultado
    url(r'^tiporesultado/add/$', login_required(TipoResultadoCreate.as_view()), name='resultadoadd'),
    url(r'^tiposresultado', login_required(TipoResultadoList.as_view()), name='resultados'),
    url(r'^tiporesultado/update/(?P<pk>\d+)/$', login_required(TipoResultadoUpdate.as_view()), name='resultadoupdate'),
    url(r'^tiporesultado/Delete/(?P<pk>\d+)/$', login_required(TipoResultadoDelete.as_view()), name='resultadoelete'),

    # Agenda

    url(r'^Agendar/$', login_required(AgendaCreate.as_view()), name='agendar'),
    url(r'^Agendados', login_required(AgendaList.as_view()), name='agendados'),
    url(r'^buscar/$', login_required(BuscarView.as_view()), name='buscar'),
    url(r'^busqueda_ajax/$', BusquedaAjaxView.as_view()),
    url(r'^Agendado/Update/(?P<pk>\d+)/$', login_required(AgendaUpdate.as_view()), name='agendaupdate'),
    url(r'^AgendaFicha/(?P<pk>\d+)/$', login_required(FichaAgenda.as_view()), name='agendaficha'),

    # Ficha CU
    url(r'^Ficha/(?P<idagendado>\d+)/$', login_required(FichaCreate), name='ficha'),

    url(r'^Buscar/$', login_required(FichaFile), name='archivar'),
    url(r'^search$', search, name='search'),
    url(r'^archivar/$', archivo.as_view(), name='archivos'),
    url(r'^ficha/update/(?P<pk>\d+)/$', login_required(Archivar.as_view()), name='fichaup'),

    # Evaluador
    url(r'^Evaluadores/add$', login_required(EvaluadorCreate.as_view()), name='evaluadoradd'),
    url(r'^Evaluadores/$', login_required(EvaluadorList.as_view()), name='evaluadores'),
    url(r'^Evaluadores/update/(?P<pk>\d+)/$', login_required(EvaluadorUpdate.as_view()), name='evaluadorupdate'),
    url(r'^Evaluadores/delete/(?P<pk>\d+)/$', login_required(EvaluadorDelete.as_view()), name='evaluadordelete'),

]
