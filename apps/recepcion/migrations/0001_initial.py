# Generated by Django 3.0.8 on 2020-07-05 03:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('idAgendado', models.AutoField(primary_key=True, serialize=False)),
                ('fechaEvaluar', models.DateField()),
                ('nombreEvaluado', models.CharField(max_length=75)),
                ('puesto', models.CharField(max_length=100)),
                ('horaProgramada', models.TimeField()),
                ('asistencia', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('codEmpresa', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('nit', models.CharField(max_length=17)),
                ('nrc', models.CharField(max_length=8)),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100, null=True)),
                ('giro', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Evaluador',
            fields=[
                ('idEvaluador', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('letra', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitado',
            fields=[
                ('idSolicitante', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoPrueba',
            fields=[
                ('idTipoPrueba', models.AutoField(primary_key=True, serialize=False)),
                ('tipoPrueba', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TipoResultado',
            fields=[
                ('idTipoResultado', models.AutoField(primary_key=True, serialize=False)),
                ('resultado', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idEmpresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recepcion.Empresa')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('idPersona', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('cargo', models.CharField(max_length=50, null=True)),
                ('idEmpresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recepcion.Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Ficha',
            fields=[
                ('idFicha', models.AutoField(primary_key=True, serialize=False)),
                ('ap', models.CharField(max_length=11)),
                ('dui', models.CharField(max_length=10)),
                ('fechaFicha', models.DateField(auto_now=True)),
                ('observaciones', models.TextField(max_length=240, null=True)),
                ('facturado', models.BooleanField(default=False)),
                ('precio', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, null=True)),
                ('idEvaluador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recepcion.Evaluador')),
                ('idProgramado', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='recepcion.Agenda')),
                ('idResultado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recepcion.TipoResultado')),
            ],
        ),
        migrations.AddField(
            model_name='agenda',
            name='idEmpresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recepcion.Empresa'),
        ),
        migrations.AddField(
            model_name='agenda',
            name='idSolicitante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recepcion.Persona'),
        ),
        migrations.AddField(
            model_name='agenda',
            name='idTipoPrueba',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recepcion.TipoPrueba'),
        ),
    ]
