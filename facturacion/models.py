from django.db import models

# Create your models here.
from apps.recepcion.models import Empresa, TipoPrueba


class Precio(models.Model):
    class Meta:
        unique_together = ('idEmpresa', 'idTipoPrueba')
        ordering = ['idEmpresa']

    idPrecio = models.AutoField(primary_key=True)
    idEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    idTipoPrueba = models.ForeignKey(TipoPrueba, on_delete=models.CASCADE)
    precio = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.precio)


class Documentos(models.Model):
    idDocumento = models.AutoField(primary_key=True)
    nombre = models.TextField(max_length=50)
    documento = models.FileField(upload_to='apempresas')
    idEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.nombre)