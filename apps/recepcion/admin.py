# Register your models here.
from django.contrib import admin
from .models import *


class QuestionAdmin(admin.ModelAdmin):
    fields = ['__all__']


admin.site.register(Agenda)
admin.site.register(Solicitado)
admin.site.register(Empresa)
admin.site.register(Persona)
admin.site.register(TipoPrueba)
admin.site.register(TipoResultado)
admin.site.register(Profile)
admin.site.register(Evaluador)
admin.site.register(Ficha)
