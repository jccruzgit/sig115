from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User


class Solicitado(models.Model):
    idSolicitante = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50, null=True)


# para empresa
class Empresa(models.Model):
    codEmpresa = models.CharField(primary_key=True, max_length=4)
    nit = models.CharField(max_length=17)
    nrc = models.CharField(max_length=8, null=False)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, null=True)
    giro = models.CharField(max_length=50, null=True)

    def __str__(self):
        return '{}'.format(self.nombre, self.direccion)


# para solicitante
class Persona(models.Model):
    idPersona = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50, null=True)
    idEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return '{} {} {}'.format(self.nombre, self.apellidos, self.idPersona)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    idEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)


# para tipos de prueba
class TipoPrueba(models.Model):
    idTipoPrueba = models.AutoField(primary_key=True)
    tipoPrueba = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.tipoPrueba)


# para agendar
class Agenda(models.Model):
    idAgendado = models.AutoField(primary_key=True)
    idEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    idSolicitante = models.ForeignKey(Persona, on_delete=models.CASCADE)
    idTipoPrueba = models.ForeignKey(TipoPrueba, on_delete=models.CASCADE)
    fechaEvaluar = models.DateField(auto_now=False, )
    nombreEvaluado = models.CharField(max_length=75)
    puesto = models.CharField(max_length=100)
    horaProgramada = models.TimeField(auto_now=False)
    asistencia = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.idAgendado)


# para TipoResultado
class TipoResultado(models.Model):
    idTipoResultado = models.AutoField(primary_key=True)
    resultado = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.resultado)


# para evaluador
class Evaluador(models.Model):
    idEvaluador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    letra = models.CharField(max_length=1)

    def __str__(self):
        return '{}'.format(self.letra)


# para ficha
class Ficha(models.Model):
    idFicha = models.AutoField(primary_key=True)
    idProgramado = models.OneToOneField(Agenda, on_delete=models.CASCADE)
    idEvaluador = models.ForeignKey(Evaluador, on_delete=models.CASCADE)
    idResultado = models.ForeignKey(TipoResultado, on_delete=models.CASCADE)
    ap = models.CharField(max_length=11)
    dui = models.CharField(max_length=10)
    fechaFicha = models.DateField(auto_now=True)
    observaciones = models.TextField(max_length=240, null=True)
    facturado = models.BooleanField(default=False)
    precio = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, null=True)

    def __str__(self):
        return '{}'.format(self.idFicha)


