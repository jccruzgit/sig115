from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from facturacion.views import CreatePrecio, ListPrecios, UpdatePrice
from facturacion.views import facturas, DetalleFactura, facturaiva, Upload_file, Download, grafica, ReportePersonasPDF

app_name ='facturacion'

urlpatterns = [
    #Precios
    url(r'^precios/$', login_required(ListPrecios.as_view()), name='precios'),
    url(r'^preciosadd/$', login_required(CreatePrecio.as_view()), name='preciosadd'),
    url(r'^preciosupdate/(?P<pk>\d+)/$', login_required(UpdatePrice.as_view()), name='preciosupdate'),

    #Facturas
    url(r'^facturar/$', login_required(facturas), name='facturar'),
    url(r'^detalle/$', login_required(DetalleFactura), name='detalle'),
    url(r'^facturaiva/$', login_required(facturaiva), name='facturaiva'),

    #Subir y Bajar Documentos
    url(r'^upload/$', login_required(Upload_file), name='upload'),
    url(r'^download/$', login_required(Download.as_view()), name='download'),

    #Grafica

    url(r'^graficas/$', login_required(grafica), name='graficas'),

    #Reporte
    url(r'^reporte_personas_pdf/$',login_required(ReportePersonasPDF.as_view()), name="reporte_personas_pdf"),

]