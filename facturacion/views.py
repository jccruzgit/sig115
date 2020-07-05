# Create your views here.
import datetime
import json as simplejson
import random
from io import BytesIO

from bootstrap_modal_forms.mixins import PassRequestMixin
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin  # mensajes con clases
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, BadHeaderError
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import View, CreateView
from django.views.generic.edit import UpdateView
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

from apps.recepcion.models import Empresa, Ficha, Profile, Evaluador
from facturacion.forms import CrearPrecioForm
from facturacion.models import Precio, Documentos
from .forms import DocumentosForm


#PRECIOS----------------------------------------------------------------------------------------------------------------
class CreatePrecio(PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'arguetaservicios/Precio/PrecioCreate.html'
    form_class = CrearPrecioForm
    success_message = 'Se registro correctamente.'
    success_url = reverse_lazy('facturacion:precios')

class UpdatePrice(PassRequestMixin, SuccessMessageMixin,UpdateView):
    model= Precio
    form_class = CrearPrecioForm
    template_name='arguetaservicios/Precio/PrecioCreate.html'
    success_url=reverse_lazy('facturacion:precios')

class ListPrecios(ListView):
    model = Precio
    template_name = 'arguetaservicios/Precio/Precios.html'
    paginate_by = 10




#Facturas---------------------------------------------------------------------------------------------------------------


def facturas(request):
    empresa = Empresa.objects.all()
    contexto = {'empresas': empresa}
    return render(request, 'arguetaservicios/Facturas/facturas.html', contexto)


def DetalleFactura(request):
    empresa = request.POST['empresa']
    desde= request.POST['desde']
    hasta=request.POST['hasta']
    emp = Empresa.objects.get(codEmpresa=empresa)
    fichas = Ficha.objects.filter(fechaFicha__range=(desde,hasta), idProgramado__idEmpresa__codEmpresa=empresa)

    aux = 0
    for ficha in fichas:
        aux = aux + ficha.precio

    iva = float(aux) * 1.13
    impuesto = float(aux) * 0.13

    context={
        'fichas': fichas,
        'desde':desde,
        'hasta': hasta,
        'emo': empresa,
        'empresa':emp,
        'monto':aux,
        'iva':iva,
        'impuesto':impuesto,
    }
    return render(request, 'arguetaservicios/Facturas/DetalleFactura.html', context)

def facturaiva(request):
    render(request, 'arguetaservicios/Facturas/facturaiva.html')


def Upload_file(request):
    if request.method == 'POST':
        form = DocumentosForm(request.POST, request.FILES, request.POST)
        if form.is_valid():
            newdoc = Documentos(documento = request.FILES['documento'], nombre=request.POST['nombre'], idEmpresa_id=request.POST['idEmpresa'])
            newdoc.save(form)

            subject = "Nuevo Informe Psicologico"
            message = "Informe Psicologico de "+newdoc.nombre+" ha sido agregado al sistema"
            message += "ver informe : https://mail.google.com/mail/u/1/#inbox"


            profile = Profile.objects.get(idEmpresa=newdoc.idEmpresa)
            usuario = User.objects.get(id=profile.user.id)
            print(usuario.email)
            from_email = "arguetaservicios@gmail.com"

            if subject and message and from_email:
                try:
                    send_mail(subject, message, from_email, [usuario.email])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return HttpResponseRedirect(reverse_lazy('recepcion:dashboard'))
            else:
                # In reality we'd use a form class
                # to get proper validation errors.
                return HttpResponse('Make sure all fields are entered and valid.')

    else:
        form = DocumentosForm()
    return render(request, 'arguetaservicios/Documentos/upload.html',{'form':form})


class Download(ListView):
    model = Documentos
    template_name = 'arguetaservicios/Documentos/download.html'
    ordering = 'idDocumento'

    def get_queryset(self):
        try:
            filtro = Profile.objects.get(user=self.request.user)
            return Documentos.objects.filter(idEmpresa_id=filtro.idEmpresa)
        except:
            return redirect('recepcion:dashboard')



def grafica(request):
    fichas = Ficha.objects.all()
    cantidad = []
    empressa = []
    color = []
    i = 0


    cantidad2 = []
    evaluador = []
    color2 = []
    j=0

    emp = Empresa.objects.all()
    for e in emp:
        pubs = Ficha.objects.filter(idProgramado__idEmpresa__codEmpresa=e.codEmpresa).count()
        cantidad.append(pubs)
        empressa.append(e.nombre)

        r = lambda: random.randint(0, 255)
        r = lambda: random.randint(0, 255)
        color.append('#%02X%02X%02X' % (r(), r(), r()))

        i +=1

    empresa = simplejson.dumps(empressa)
    numero = simplejson.dumps(cantidad)
    colores = simplejson.dumps(color)

    pol = Evaluador.objects.all()
    for p in pol:
        cont = Ficha.objects.filter(idEvaluador =p.idEvaluador).count()
        cantidad2.append(cont)
        evaluador.append(p.nombre)
        r = lambda: random.randint(0, 255)
        r = lambda: random.randint(0, 255)
        color2.append('#%02X%02X%02X' % (r(), r(), r()))

        j += 1


    poli = simplejson.dumps(evaluador)
    numero2 = simplejson.dumps(cantidad2)
    colores2 = simplejson.dumps(color2)

    context = {
            'empresas': empresa,
            'cantidad': numero,
            'color': color,
            'i': i,
            'evaluadores': poli,
            'numero2': numero2,
            'colores2': colores2,
            'j':j
        }

    return render(request,'arguetaservicios/Graficas/grafica.html', context)


class ReportePersonasPDF(View):

    def cabecera(self, pdf,emp,des,has,tip):
        # Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT + '\imagenes\pdf.png'
        # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 200, 675, 200, 200, preserveAspectRatio=True)

        # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Helvetica", 20)
        # Dibujamos una cadena en la ubicación X,Y especificada
        pdf.drawString(30, 700, u"ARGUETA SERVICIOS S.A de C.V")
        pdf.setFont("Helvetica", 14)

        if tip == 'cc':
            pdf.drawString(200, 680, u"Factura Consumidor Final")
        elif tip=='cf':
            pdf.drawString(200, 680, u"Factura Credito Fiscal")

            pdf.setFont("Helvetica", 12)
            pdf.drawString(30, 640, u"Empresa : ")

            empresa = Empresa.objects.get(codEmpresa=emp)

            pdf.setFont("Helvetica", 12)
            pdf.drawString(90, 640, u" " + empresa.nombre)

            pdf.drawString(30, 625, u"Direccion : ")
            pdf.drawString(90, 625, u" " + empresa.direccion)

            pdf.drawString(30, 610, u"NRC : ")
            pdf.drawString(90, 610, u" " + empresa.nrc)

            pdf.drawString(380, 640, u"Fecha : ")
            pdf.drawString(430, 640, u" " + datetime.datetime.today().strftime('%d/%m/%Y'))

            pdf.drawString(30, 595, u"NIT : ")
            pdf.drawString(90, 595, u" " + empresa.nit)

        else:
            pdf.drawString(200, 680, u"Factura Manofactura")

            pdf.setFont("Helvetica", 12)
            pdf.drawString(30, 640, u"Empresa : ")

            empresa = Empresa.objects.get(codEmpresa=emp)
            pdf.setFont("Helvetica", 12)
            pdf.drawString(90, 640, u" " + empresa.nombre)

            pdf.drawString(30, 625, u"Direccion : ")
            pdf.drawString(90, 625, u" " + empresa.direccion)

            pdf.drawString(30, 610, u"NRC: ")
            pdf.drawString(90, 610, u" " + empresa.nrc )

            pdf.drawString(350, 640, u"Fecha : ")
            pdf.drawString(400, 640, u" " + datetime.datetime.today().strftime('%d/%m/%Y'))

            pdf.drawString(30, 595, u"NIT : ")
            pdf.drawString(90, 595, u" " + empresa.nit)





    def get(self, request, *args, **kwargs):

        emp = request.GET['emo']
        des = request.GET['desde']
        has = request.GET['hasta']
        tip = request.GET['tipo']

        # Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        # La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        # Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)
        # Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf,emp,des,has,tip)
        # Con show page hacemos un corte de página para pasar a la siguiente
        y=600

        if tip=="cf":
            self.tabla(pdf, y, emp, des, has, tip)
        elif tip =="cc":
            self.tabla2(pdf, y, emp, des, has, tip)
        else:
            self.tabla3(pdf, y, emp, des, has, tip)

        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    def tabla(self, pdf, y, emp,des,has,tip):
        fichas = Ficha.objects.filter(fechaFicha__range=(des, has), idProgramado__idEmpresa__codEmpresa=emp)
        cantidad = fichas.count()

        total = 0
        for ficha in fichas:
            total = total + ficha.precio
        iv = total
        total= round((float(total)* 1.13), 2)
        iva= round((float(iv)*0.13),2)

        #consumidor final

        informacion = [
            (
                1,
                "PSICOMETRIA " +f.idProgramado.idTipoPrueba.tipoPrueba,
                f.precio,
                "",
                "",
                round((float(f.precio)*0.13),2),
                round(float(f.precio)+round((float(f.precio)*0.13),2),2)

            ) for f in Ficha.objects.filter(fechaFicha__range=(des, has), idProgramado__idEmpresa__codEmpresa=emp)]

        # Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Cant', 'Descripcion', 'Precio Unitario', 'Ventas N/SUJ', 'VTA EXEN',"IVA",'VENTAS GRABADAS' )
        # Creamos una lista de tuplas que van a contener a las personas
        detalles = [(" ", " ", " ", " ", "", "", ""),
                    (" ", " ", " ", " ","", "Suma $", total),
                    (" ", " ", " ", " ", "","IVA retenido $", ""),
                    (" ", " ", " ", " ","", "Sub total $", ""),
                    (" ", " ", " ", " ","", "Ventas N/SUJ $", ""),
                    (" ", " ", " ", " ","", "Ventas Exentas $", ""),
                    (" ", " ", " ", " ","", "Total $", total),
                    ]




        # Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados]+informacion + detalles, colWidths=[25 , 110,70 ,70, 80,90,110 ])
        # Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                # La primera fila(encabezados) va a estar centrada
                ('ALIGN', (0, 0), (3, 0), 'CENTER'),
                # Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                # El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))
        # Establecemos el tamaño de la hoja que ocupará la tabla
        detalle_orden.wrapOn(pdf, 800, 600)
        # Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 20, 300)

    def tabla2(self, pdf, y, emp, des, has, tip):
        fichas = Ficha.objects.filter(fechaFicha__range=(des, has), idProgramado__idEmpresa__codEmpresa=emp)
        cantidad = fichas.count()

        total = 0
        for ficha in fichas:
            total = total + ficha.precio
        iv = total
        total = round((float(total) * 1.13), 2)
        iva = round((float(iv) * 0.13), 2)

        # consumidor final

        informacion = [
            (
                1,
                "PSICOMETRIA " + f.idProgramado.idTipoPrueba.tipoPrueba,
                round(float(f.precio)+round((float(f.precio)*0.13),2),2)
                ,
                "",
                "",
                round(float(f.precio) + round((float(f.precio) * 0.13), 2), 2)
            ) for f in Ficha.objects.filter(fechaFicha__range=(des, has), idProgramado__idEmpresa__codEmpresa=emp)]

        # Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Cant', 'Descripcion', 'Precio Unitario', 'Ventas N/SUJ', 'VTA EXEN', 'VENTAS GRABADAS')
        # Creamos una lista de tuplas que van a contener a las personas
        detalles = [(" ", " ", " ", " ", "", ""),
                    (" ", " ", " ", "", "Suma $", total),
                    (" ", " ", " ", "", "IVA retenido $", ""),
                    (" ", " ", " ", "", "Sub total $", ""),
                    (" ", " ", " ", "", "Ventas N/SUJ $", ""),
                    (" ", " ", " ", "", "Ventas Exentas $", ""),
                    (" ", " ", " ", "", "Total $", total),
                    ]

        # Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados] + informacion + detalles, colWidths=[25, 110, 70, 80, 90, 110])
        # Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                # La primera fila(encabezados) va a estar centrada
                ('ALIGN', (0, 0), (3, 0), 'CENTER'),
                # Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                # El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))
        # Establecemos el tamaño de la hoja que ocupará la tabla
        detalle_orden.wrapOn(pdf, 800, 600)
        # Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 50, 400)


    def tabla3(self, pdf, y, emp, des, has, tip):
        fichas = Ficha.objects.filter(fechaFicha__range=(des, has), idProgramado__idEmpresa__codEmpresa=emp)
        cantidad = fichas.count()

        total = 0
        retenido = 0
        for ficha in fichas:
            total = total + ficha.precio
            retenido =retenido + round((float(ficha.precio) * 0.13), 2)

        iv = total
        total = round((float(total) * 1.13), 2)
        iva = round((float(iv) * 0.13), 2)
        final = total-retenido
        # consumidor final

        informacion = [
            (
                1,
                "Psicometria " + f.idProgramado.idTipoPrueba.tipoPrueba,
                f.precio,
                "",
                "",
                round((float(f.precio) * 0.13), 2),
                round(float(f.precio) + round((float(f.precio) * 0.13), 2), 2)

            ) for f in Ficha.objects.filter(fechaFicha__range=(des, has), idProgramado__idEmpresa__codEmpresa=emp)]

        # Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Cant', 'Descripcion', 'Precio Unitario', 'Ventas N/SUJ', 'VTA EXEN', "IVA", 'VENTAS GRABADAS')
        # Creamos una lista de tuplas que van a contener a las personas
        detalles = [(" ", " ", " ", " ", "", "", ""),
                    (" ", " ", " ", " ", "", "Suma $", total),
                    (" ", " ", " ", " ", "", "IVA retenido $", retenido),
                    (" ", " ", " ", " ", "", "Sub total $", ""),
                    (" ", " ", " ", " ", "", "Ventas N/SUJ $", ""),
                    (" ", " ", " ", " ", "", "Ventas Exentas $", ""),
                    (" ", " ", " ", " ", "", "Total $", final),
                    ]

        # Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados] + informacion + detalles, colWidths=[25, 110, 70, 70, 80, 90, 110])
        # Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                # La primera fila(encabezados) va a estar centrada
                ('ALIGN', (0, 0), (3, 0), 'CENTER'),
                # Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                # El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))
        # Establecemos el tamaño de la hoja que ocupará la tabla
        detalle_orden.wrapOn(pdf, 800, 600)
        # Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 20, 300)



