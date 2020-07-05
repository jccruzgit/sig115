from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.shortcuts import render
from ArguetaServicios import settings

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy


def home(request):
    return render(request, 'home.html')


def contactanos(request):
    return render(request, 'contactanos.html')


def service(request):
    return render(request, 'servicios.html')


def we(request):
    return render(request, 'nosotros.html')


def send_email(request):
    subject = request.POST.get('asunto')
    message = "Correo :" + request.POST.get('correo') + "\n"
    message += "Mensaje :" + request.POST.get('mensaje')
    from_email = request.POST.get('correo')
    settings.EMAIL_HOST_USER = from_email

    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['arguetaservicios@gmail.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect(reverse_lazy('contactanos'))
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')
