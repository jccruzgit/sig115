"""ArguetaServicios URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, \
    PasswordResetConfirmView

from facturacion.views import CreatePrecio, ListPrecios, UpdatePrice,facturaiva
from facturacion.views import facturas, DetalleFactura, Upload_file, Download, grafica, ReportePersonasPDF
from apps.recepcion.views import LoginClass
from .views import home
from .views import contactanos, send_email
from .views import service
from .views import we


app_name = 'ArguetaServicios'

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^contactanos$', contactanos, name='contactanos'),
    url(r'^servicios$', service, name='servicios'),
    url(r'^nosotros$', we, name='nosotros'),
    url('admin/', admin.site.urls),
    url(r'^apps.recepcion/', include('apps.recepcion.urls')),  # App recepcion
    url(r'^ArguetaServicios/', include('facturacion.urls')),  # App facturacion y reportes
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^accounts/login/', LoginClass.as_view(), name='login'),
    url(r'^email/', send_email, name="send"),

    url(r'^registration/password_reset', PasswordResetView.as_view(),{'subject_template_name': 'registration'
                                                                                               '/password_reset_form.html',
         'email_template_name': 'registration/password_reset_email.html'}, name='password_reset'),

    url(r'^password_reset_done', PasswordResetDoneView.as_view(),{'template_name': 'registration/password_reset_done'
                                                                                   '.html'},
        name='password_reset_done'),

    url(r'^registration/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', PasswordResetConfirmView.as_view(),{'template_name': 'registration/password_reset_confirm.html'}, name='password_reset_confirm'),

    url(r'^registration/done', PasswordResetCompleteView.as_view(),{'template_name': 'registration'
                                                                                     '/password_reset_complete.html'}, name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
