"""vulnerable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin

from django.urls import path, include
from camara import views

from admisiones import views as viewsAdmisiones

from django.conf  import settings
from django.conf.urls.static import  static
from clinico import views as viewsClinico
#from mecanicosPacientes import views as viewsmecanicosPacientes


urlpatterns = [
    path('admin/', admin.site.urls),
    path('acceso/', views.acceso),

    # Acceso al Programa

    path('menu/', views.menu),
    # path('menuAcceso/validaAcceso/', views.validaAcceso),
    path('contrasena/<str:documento>', views.contrasena),
    # path('salir/validaAcceso/', views.validaAcceso),

    # HISTORIA CLINICA

    path('accesoEspecialidadMedico/historiaView/<str:documento>', viewsClinico.nuevoView.as_view()),
    path('historia1View/', viewsClinico.historia1View),
    path('historiaExamenesView/', viewsClinico.historiaExamenesView),
    path('consecutivo_folios/', viewsClinico.consecutivo_folios),
    path('buscaExamenes/', viewsClinico.buscaExamenes),
    path('motivoSeñas/', viewsClinico.motivoSeñas),
    path('subjetivoSeñas/', viewsClinico.subjetivoSeñas),
    path('motivoInvidente/', viewsClinico.motivoInvidente),
    # path('resMotivoInvidente/', viewsClinico.s),
    path('reconocerAudio/', views.reconocerAudio),
    path('reproduceAudio/', views.reproduceAudio),
    path('accesoEspecialidadMedico/<str:documento>', views.accesoEspecialidadMedico),

    # Actividaes Mecanicas

    path('prueba/', viewsClinico.prueba),
 #   path('manejoLuz/', viewsmecanicosPacientes.manejoLuz.as_view()),
  #  path('ambienteMusical/', viewsmecanicosPacientes.ambienteMusical.as_view()),
    path('camara/', views.camara),
    path('leeAudio/', views.leeAudio),

    # Admisiones

    path('admHospProvisional/<str:Documento>,<str:Perfil>,<str:Sede>,<str:Servicio>',
         viewsAdmisiones.admHospProvisional),

    path('chaining/', include('smart_selects.urls')),
    path('menuAcceso/', viewsAdmisiones.menuAcceso),
    path('validaAcceso/', viewsAdmisiones.validaAcceso),

    path('retornarAdmision/<str:Sede>,<str:Perfil> , <str:Username>, <str:Username_id>', viewsAdmisiones.retornarAdmision),

    path('salir/', viewsAdmisiones.salir),
    path('grabar1/<str:username>,<str:contrasenaAnt>,<str:contrasenaNueva>,<str:contrasenaNueva2>',
         viewsAdmisiones.validaPassword),
    path('findOne/<str:username> , <str:password> , <str:tipoDoc>/', viewsAdmisiones.Modal),
    # path('buscarAdmision/<str:BusHabitacion>,<str:BusTipoDoc>,<str:BusDocumento>,<str:BusPaciente>,<str:BusDesde>,<str:BusHasta>', viewsAdmisiones.buscarAdmision),
    path('buscarAdmision/', viewsAdmisiones.buscarAdmision),
    path('guardarAdmision/', viewsAdmisiones.guardarAdmision),

    path('buscarHabitaciones/', viewsAdmisiones.buscarHabitaciones),
    path('crearAdmision/<str:Sede>,<str:Perfil>, <str:Username>, <str:Username_id>', viewsAdmisiones.crearAdmision.as_view()),
    path('crearResponsables/', viewsAdmisiones.crearResponsables),

    # Facturacion

    # Citas Medicas

]

if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)