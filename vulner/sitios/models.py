from django.db import models
from django.utils.timezone import now


from smart_selects.db_fields import GroupedForeignKey
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.




class Departamentos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
  #  usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre

class Ciudades(models.Model):
        id = models.AutoField(primary_key=True)
        departamentos = models.ForeignKey('sitios.Departamentos', default=1, on_delete=models.PROTECT, null=True, related_name = 'ciudades')
        nombre = models.CharField(max_length=50)
        fechaRegistro = models.DateTimeField(default=now, editable=False)
   #     usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
        estadoReg = models.CharField(max_length=1, default='A', editable=False)

        def __str__(self):
            return self.nombre

class SedesClinica(models.Model):
    id = models.AutoField(primary_key=True)

    departamentos = models.ForeignKey('sitios.Departamentos', default=1, on_delete=models.PROTECT, null=True)
    ciudades = ChainedForeignKey(Ciudades, chained_field='departamentos', chained_model_field='departamentos',
                                 show_all=False)
    nombre = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    contacto = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
 #   usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1,default='A', editable=False)

    def __str__(self):
        return self.nombre




class Centros(models.Model):
        id = models.AutoField(primary_key=True)
        nombre = models.CharField(max_length=50)
        departamentos = models.ForeignKey('sitios.Departamentos', default=1, on_delete=models.PROTECT, null=True)

        ciudades = ChainedForeignKey(Ciudades, chained_field='departamentos', chained_model_field='departamentos',
                                     show_all=False)


        ubicacion = models.CharField(max_length=50, default='')
        direccion = models.CharField(max_length=50)
        telefono = models.CharField(max_length=20)
        contacto = models.CharField(max_length=50)
        fechaRegistro = models.DateTimeField(default=now, editable=False)
     #   usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
        estadoReg = models.CharField(max_length=1, default='A', editable=False)


        def __str__(self):
                return self.nombre


class DependenciasTipo(models.Model):
        id = models.AutoField(primary_key=True)
        nombre = models.CharField(max_length=50)


        def __str__(self):
             return self.nombre

class ServiciosSedes(models.Model):

    id = models.AutoField(primary_key= True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', default=1, on_delete=models.PROTECT, null=True)
    servicios = models.ForeignKey('clinico.Servicios', default=1, on_delete=models.PROTECT, null=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sedesClinica', 'servicios'],
                                    name='Constraint_ServiciosSedes')
        ]



    def __str__(self):
             return self.nombre



class Dependencias(models.Model):
    id = models.AutoField(primary_key=True)
    dependenciasTipo= models.ForeignKey('sitios.DependenciasTipo', default=1, on_delete=models.PROTECT, null=True)
    serviciosSedes = models.ForeignKey('sitios.ServiciosSedes', default=1, on_delete=models.PROTECT, null=True, related_name ='serviciosSedes1')
    sedesClinica = models.ForeignKey('sitios.SedesClinica', default=1, on_delete=models.PROTECT, null=True)
    servicios = models.ForeignKey('clinico.Servicios', default=1, on_delete=models.PROTECT, null=True)

    servicios = ChainedForeignKey(ServiciosSedes, chained_field='servicios', chained_model_field='servicios',
                                 show_all=False)
    numero =  models.CharField(max_length=50, default="")
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
   # usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=[ 'sedesClinica', 'servicios','dependenciasTipo','numero'], name='Constraint_dependencias')
        ]

    def __str__(self):
        return self.nombre


class DependenciasActual(models.Model):
    id = models.AutoField(primary_key=True)
    dependencias = models.ForeignKey('sitios.Dependencias', default=1, on_delete=models.PROTECT, null=True)
    tipoDoc= models.ForeignKey('usuarios.TiposDocumento', default=1, on_delete=models.PROTECT, null=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    documento	= models.IntegerField()
    consec	= models.IntegerField()
    fechaRegistro = models.DateTimeField(default=now, editable=False)
  #  usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)


    def __str__(self):
        return self.nombre