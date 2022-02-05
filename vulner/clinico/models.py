from django.db import models
from django.utils.timezone import now

# Create your models here.




class Servicios(models.Model):
    id = models.AutoField(primary_key=True)
    #sedesClinica = models.ForeignKey('sitios.SedesClinica', default=1, on_delete=models.PROTECT, null=True)
    nombre = models.CharField(max_length=30)


    def __str__(self):
        return self.nombre

class EspecialidadesMedicos(models.Model):
    id = models.AutoField(primary_key=True)
    id_especialidad = models.ForeignKey('Especialidades', on_delete=models.PROTECT, null=True)
    id_medico = models.ForeignKey('planta.Planta', on_delete = models.PROTECT, null = True)

    def __integer__(self):
        return self.id_medico


class Especialidades(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

class Medicos(models.Model):
        id = models.AutoField(primary_key=True)
        id_tipo_doc = models.ForeignKey('usuarios.TiposDocumento', default=1, on_delete=models.PROTECT, null=True)
        documento = models.IntegerField(default=1)
        nombre = models.CharField(max_length=30)
        id_especialidad = models.ForeignKey('clinico.Especialidades', default=1, on_delete=models.PROTECT, null=True)
        id_departamento = models.ForeignKey('sitios.Departamentos', default=1, on_delete=models.PROTECT, null=True)
        id_ciudad = models.ForeignKey('sitios.Ciudades', default=1, on_delete=models.PROTECT, null=True)
        direccion = models.CharField(max_length=50)
        telefono = models.CharField(max_length=20)
        contacto = models.CharField(max_length=50)
        id_centro = models.ForeignKey('sitios.Centros', default=1, on_delete=models.PROTECT, null=True)
        estado = models.CharField(max_length=1)

        def __str__(self):
            return self.nombre

class TiposExamen(models.Model):
            id = models.AutoField(primary_key=True)
            nombre = models.CharField(max_length=30)

            def __str__(self):
                return self.nombre

class Examenes(models.Model):
                id = models.AutoField(primary_key=True)
                id_TipoExamen = models.ForeignKey('clinico.TiposExamen', default=1, on_delete=models.PROTECT, null=True)
                nombre = models.CharField(max_length=30)

                def __str__(self):
                    return self.nombre




class Historia(models.Model):
                id = models.AutoField(primary_key=True)
                id_tipo_doc = models.ForeignKey('usuarios.TiposDocumento', default=1, on_delete=models.PROTECT,null=True)
                documento = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT,null=True)
                folio =  models.IntegerField(default=0)
                fecha = models.DateTimeField()
                id_especialidad = models.ForeignKey('clinico.Especialidades', default=1, on_delete=models.PROTECT, null=True)
                id_medico  = models.ForeignKey('clinico.Medicos', default=1, on_delete=models.PROTECT, null=True)
                motivo     = models.CharField(max_length=250, default='')
                subjetivo  = models.CharField(max_length=250, default='')
                objetivo   = models.CharField(max_length=250, default='')
                analisis   = models.CharField(max_length=250, default='')
                plan       = models.CharField(max_length=250, default='')
                estado_folio = models.CharField(max_length=1, default='A')

                def __str__(self):
                    return self.motivo

                class Meta:
                    ordering = ["id_tipo_doc","documento","folio","fecha","id_especialidad","id_medico","motivo","subjetivo","objetivo","analisis","plan"]

class HistoriaExamenes(models.Model):
                id = models.AutoField(primary_key=True)
                id_tipo_doc = models.ForeignKey('usuarios.TiposDocumento', default=1, on_delete=models.PROTECT, null=True)
                documento = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT,null=True)
                folio = models.IntegerField()
                fecha = models.DateTimeField()
                id_TipoExamen = models.ForeignKey('clinico.TiposExamen', default=1, on_delete=models.PROTECT, null=True)
                id_examen = models.ForeignKey('clinico.Examenes', default=1, on_delete=models.PROTECT, null=True)
                cantidad  = models.IntegerField()
                estado_folio = models.CharField(max_length=1, default='A')

                def __str__(self):
                        return self.estado_folio

class HistoriaResultados(models.Model):
                    id = models.AutoField(primary_key=True)
                    id_tipo_doc = models.ForeignKey('usuarios.TiposDocumento', default=1, on_delete=models.PROTECT, null=True)
                    documento = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT,null=True)
                    folio = models.IntegerField()
                    fecha = models.DateTimeField()
                    consecutivo = models.IntegerField()
                    id_TipoExamen = models.ForeignKey('clinico.TiposExamen', default=1, on_delete=models.PROTECT,
                                                      null=True)
                    id_examen = models.ForeignKey('clinico.Examenes', default=1, on_delete=models.PROTECT, null=True)
                    cantidad = models.IntegerField()
                    resultado = models.CharField(max_length=500, default='')
                    estado  = models.CharField(max_length=1, default='A')

                    def __str__(self):
                        return self.resultado


class Diagnosticos(models.Model):
    id = models.AutoField(primary_key=True)
    cie10  = models.CharField(max_length=15, default='')
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=80)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    #usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre


class EstadosSalida(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre