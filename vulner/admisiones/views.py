from django.shortcuts import render
import MySQLdb
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import json
from django.views.generic import ListView, CreateView, TemplateView
from .forms import crearAdmisionForm
from datetime import datetime
from admisiones.models import Ingresos
from django.db.models import Max

# Create your views here.


def menuAcceso(request):
    print("Ingreso a acceso")


    miConexion = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM planta_tiposPlanta"
    cur.execute(comando)
    print(comando)

    perfiles = []
    context = {}

    for id, nombre in cur.fetchall():
        perfiles.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(perfiles)

    context['Perfiles'] = perfiles

    miConexion = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM sitios_sedesClinica"
    cur.execute(comando)
    print(comando)

    sedes = []


    for id, nombre in cur.fetchall():
        sedes.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(sedes)

    context['Sedes'] = sedes



    return render(request, "accesoPrincipal.html", context)



def validaAcceso(request):
    print("Hola Entre a validar el acceso Principal")

    username = request.POST["username"]
    print("username = ", username)
    contrasena = request.POST["password"]
    perfilConseguido = request.POST["seleccion1"]
    sede = request.POST["seleccion2"]
    Sede = sede
    print("Sede Mayuscula = ", Sede)
    print(contrasena)
    print("perfil= ", perfilConseguido)
    print("sede= ", sede)
    context = {}
    context['Documento'] = username
    context['Perfil'] = perfilConseguido
    context['Sede'] = sede

    # Variables que tengo en context : Documento, Perfil , Sede,   sedes ,NombreSede

    print (context['Documento'])

    # Consigo la sede Nombre

    miConexion = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    cur = miConexion.cursor()
    comando = "SELECT id, nombre   FROM sitios_sedesClinica WHERE id ='" + sede + "'"
    cur.execute(comando)
    print(comando)

    nombreSedes = []


    for id, nombre  in cur.fetchall():
        nombreSedes.append({'id':id , 'nombre' : nombre})

    miConexion.close()
    print(nombreSedes)

    context['NombreSede'] =  nombreSedes




    # esta consulta por que se pierde de otras pantallas

    miConexion = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM sitios_sedesClinica"
    cur.execute(comando)
    print(comando)

    sedes = []

    for id, nombre in cur.fetchall():
        sedes.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(sedes)

    context['Sedes'] = sedes


    miConexion = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM planta_tiposPlanta"
    cur.execute(comando)
    print(comando)

    perfiles = []


    for id, nombre in cur.fetchall():
        perfiles.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(perfiles)

    context['Perfiles'] = perfiles

    miConexion0 = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    cur0 = miConexion0.cursor()
    comando = "select p.id  Username_id , p.nombre nombre from planta_planta p where p.documento ='" + username + "'"
    cur0.execute(comando)
    print(comando)
    planta = []

    for Username_id, nombre in cur0.fetchall():
        planta.append({'Username_id': Username_id, 'nombre': nombre})
        context['Username_id'] = Username_id

    if planta == []:


        context['Error'] = "Personal invalido ! "
        print("Entre por personal No encontrado")

        miConexion0.close()

        return render(request, "accesoPrincipal.html", context)

    else:

        print("Username_id", Username_id)

        miConexion1 = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
        cur1 = miConexion1.cursor()
        comando = "select p.contrasena contrasena from planta_planta p where p.documento ='" + username + "'" + " AND contrasena = '" + contrasena +"'"
        cur1.execute(comando)

        plantaContrasena = []

        for nombre in cur1.fetchall():
            plantaContrasena.append({'contrasena': contrasena})

        if plantaContrasena == []:
            miConexion1.close()
            context['Error'] = "Contraseña invalida ! "
            return render(request, "accesoPrincipal.html", context)
        else:


            miConexion2 = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
            cur2 = miConexion1.cursor()
            comando = "select perf.tiposPlanta_id  perfil from planta_planta p , planta_perfilesplanta perf , planta_tiposPlanta tp where p.sedesClinica_id ='" + str(sede) + "' AND p.documento =  '" + str(username) + "' AND tp.id =perf.tiposPlanta_id AND  perf.tiposPlanta_id = " + str(perfilConseguido)
            print(comando)
            cur2.execute(comando)

            perfil = []

            for perfil in cur2.fetchall():
                plantaContrasena.append({'perfil': perfil})


            if perfil == []:
                miConexion0.close()
                miConexion1.close()
                miConexion2.close()
                context['Error'] = "Perfil No autorizado ! "
                return render(request, "accesoPrincipal.html", context)


            else:

                ingresos = []

                miConexionx = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
                curx = miConexionx.cursor()

              #  detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , dxIngreso_id FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp  WHERE i.sedesClinica_id = dep.sedesClinica_id AND i.serviciosActual_id = dep.servicios_id AND i.serviciosActual_id = ser.id  AND i.dependenciasActual_id = dep.id AND i.sedesClinica_id= '" +  str(Sede) + "' AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id"

                #detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag  WHERE i.sedesClinica_id = dep.sedesClinica_id AND i.serviciosActual_id = dep.servicios_id AND i.serviciosActual_id = ser.id  AND i.dependenciasActual_id = dep.id AND  i.dependenciasIngreso_id = dep.id AND i.sedesClinica_id= '" + str( Sede) + "' AND dep.sedesClinica_id = i.sedesClinica_id AND i.sedesClinica_id = ser.sedesClinica_id AND deptip.id = dep.dependenciasTipo_id  AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id and diag.id = i.dxactual_id"
                detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd  WHERE sd.sedesClinica_id = i.sedesClinica_id  and   sd.servicios_id  = ser.id and  i.sedesClinica_id = dep.sedesClinica_id AND i.dependenciasActual_id = dep.id AND i.sedesClinica_id= '" + str(Sede) + "'  AND  deptip.id = dep.dependenciasTipo_id and dep.servicios_id = ser.id AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id and u.id = i.documento_id and diag.id = i.dxactual_id"
                print(detalle)

                curx.execute(detalle)

                for tipoDoc, documento, nombre, consec, fechaIngreso, fechaSalida, servicioNombreIng, camaNombreIng, dxActual in curx.fetchall():
                    ingresos.append({'tipoDoc': tipoDoc, 'Documento': documento, 'Nombre': nombre, 'Consec': consec,
                                     'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida,
                                     'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                                     'DxActual': dxActual})

                miConexionx.close()
                print(ingresos)
                context['Ingresos'] = ingresos

                # Combo de Servicios
                miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
                curt = miConexiont.cursor()
                comando = "SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed.sedesClinica_id ='" + str(sede) + "' AND sed.servicios_id = ser.id"
                curt.execute(comando)
                print(comando)

                servicios = []
                servicios.append({'id':'' , 'nombre': ''})

                for id, nombre in curt.fetchall():
                    servicios.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(servicios)

                context['Servicios'] = servicios

                # Fin combo servicios

                # Combo TiposDOc
                miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
                curt = miConexiont.cursor()
                comando = "SELECT id ,nombre FROM usuarios_TiposDocumento "
                curt.execute(comando)
                print(comando)

                tiposDoc = []
                tiposDoc.append({'id': '', 'nombre': ''})



                for id, nombre in curt.fetchall():
                    tiposDoc.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(tiposDoc)

                context['TiposDoc'] = tiposDoc

                # Fin combo TiposDOc

                # Combo Habitaciones
                miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
                curt = miConexiont.cursor()
                comando = "SELECT id ,nombre FROM sitios_dependencias where sedesClinica_id = '" + str(Sede) +"' AND dependenciasTipo_id = 1"
                curt.execute(comando)
                print(comando)

                habitaciones = []

                for id, nombre in curt.fetchall():
                    habitaciones.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(habitaciones)

                context['Habitaciones'] = habitaciones

                # Fin combo Habitaciones

                # Combo Especialidades
                miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
                curt = miConexiont.cursor()
                comando = "SELECT id ,nombre FROM clinico_Especialidades"
                curt.execute(comando)
                print(comando)

                especialidades = []
                especialidades.append({'id': '', 'nombre': ''})


                for id, nombre in curt.fetchall():
                    especialidades.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(especialidades)

                context['Especialidades'] = especialidades

                # Fin combo Especialidades

                # Combo Medicos
                miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
                curt = miConexiont.cursor()
                comando = "SELECT p.id id, p.nombre  nombre FROM planta_planta p ,  planta_perfilesplanta perf WHERE perf.sedesClinica_id = '" + str(Sede) + "' AND perf.tiposPlanta_id = 6 "

                curt.execute(comando)
                print(comando)

                medicos = []
                medicos.append({'id': '', 'nombre': ''})


                for id, nombre in curt.fetchall():
                    medicos.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(medicos)

                context['Medicos'] = medicos

                # Fin combo Medicos


                print("passe")

                print (perfil[0])

                if (perfil[0] == 1):
                    miConexion0.close()
                    miConexion1.close()
                    miConexion2.close()
                    print("voy para ")
                    return render(request, "clinico/menuMedico.html", context)
                if (perfil[0] == 2):
                    miConexion0.close()
                    miConexion1.close()
                    miConexion2.close()
                    return render(request, "clinico/menuEnfermero.html", context)
                if (perfil[0] == 3):
                    miConexion0.close()
                    miConexion1.close()
                    miConexion2.close()
                    return render(request, "clinico/menuAuxiliar.html", context)
                if (perfil[0] == 4):
                    miConexion0.close()
                    miConexion1.close()
                    miConexion2.close()
                    return render(request, "citasMedicas/menuCitasMedicas.html")
                if (perfil[0] == 5):
                    miConexion0.close()
                    miConexion1.close()
                    miConexion2.close()
                    return render(request, "facturacion/menuFacturacion.html", context)

                if (perfil[0] == 6):
                    miConexion0.close()
                    miConexion1.close()
                    miConexion2.close()
                    return render(request, "admisiones/panelHospAdmisionesBravo.html", context)

    return render(request, "menuMedico.html",context)



def retornarAdmision(request, Sede, Perfil, Username, Username_id):


    print ("Entre Retornar Admision")
    #Sede = request.POST["Sede"]
    print ("Sede = ", Sede)
    Sede = Sede.lstrip()
    sede = Sede
    #Perfil = request.POST["Perfil"]
    print ("Perfil = ",Perfil)
    Perfil = Perfil.lstrip()
    print("Perfil = ", Perfil)

    context = {}

    context['Sede'] = Sede
    context['Username'] = Username
    context['Username_id'] = Username_id


    # Consigo la sede Nombre

    miConexion = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    cur = miConexion.cursor()
    comando = "SELECT nombre   FROM sitios_sedesClinica WHERE id ='" + sede + "'"
    cur.execute(comando)
    print(comando)

    nombreSedes = []

    for nombre in cur.fetchall():
        nombreSedes.append({'nombre': nombre})

    miConexion.close()
    print(nombreSedes)
    nombresede1 = nombreSedes[0]

    context['NombreSede'] = nombresede1

    # esta consulta por que se pierde de otras pantallas

    miConexion = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM sitios_sedesClinica"
    cur.execute(comando)
    print(comando)

    sedes = []

    for id, nombre in cur.fetchall():
        sedes.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(sedes)

    context['Sedes'] = sedes

    ingresos = []

    miConexionx = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    curx = miConexionx.cursor()

    #  detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , dxIngreso_id FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp  WHERE i.sedesClinica_id = dep.sedesClinica_id AND i.serviciosActual_id = dep.servicios_id AND i.serviciosActual_id = ser.id  AND i.dependenciasActual_id = dep.id AND i.sedesClinica_id= '" +  str(Sede) + "' AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id"

    # detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag  WHERE i.sedesClinica_id = dep.sedesClinica_id AND i.serviciosActual_id = dep.servicios_id AND i.serviciosActual_id = ser.id  AND i.dependenciasActual_id = dep.id AND  i.dependenciasIngreso_id = dep.id AND i.sedesClinica_id= '" + str( Sede) + "' AND dep.sedesClinica_id = i.sedesClinica_id AND i.sedesClinica_id = ser.sedesClinica_id AND deptip.id = dep.dependenciasTipo_id  AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id and diag.id = i.dxactual_id"
    detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag  WHERE i.sedesClinica_id = dep.sedesClinica_id AND i.dependenciasActual_id = dep.id AND i.sedesClinica_id= '" + str(
        Sede) + "'   AND deptip.id = dep.dependenciasTipo_id and dep.servicios_id = ser.id AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id and u.id = i.documento_id and diag.id = i.dxactual_id"
    print(detalle)

    curx.execute(detalle)

    for tipoDoc, documento, nombre, consec, fechaIngreso, fechaSalida, servicioNombreIng, camaNombreIng, dxActual in curx.fetchall():
        ingresos.append({'tipoDoc': tipoDoc, 'Documento': documento, 'Nombre': nombre, 'Consec': consec,
                         'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida,
                         'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                         'DxActual': dxActual})

    miConexionx.close()
    print(ingresos)
    context['Ingresos'] = ingresos

    # Combo de Servicios
    miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    curt = miConexiont.cursor()
    comando = "SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed.sedesClinica_id ='" + str(
        sede) + "' AND sed.servicios_id = ser.id"
    curt.execute(comando)
    print(comando)

    servicios = []
    servicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        servicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(servicios)

    context['Servicios'] = servicios

    # Fin combo servicios

    # Combo TiposDOc
    miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM usuarios_TiposDocumento "
    curt.execute(comando)
    print(comando)

    tiposDoc = []
    tiposDoc.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposDoc.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposDoc)

    context['TiposDoc'] = tiposDoc

    # Fin combo TiposDOc

    # Combo Habitaciones
    miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM sitios_dependencias where sedesClinica_id = '" + str(
        Sede) + "' AND dependenciasTipo_id = 1"
    curt.execute(comando)
    print(comando)

    habitaciones = []

    for id, nombre in curt.fetchall():
        habitaciones.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(habitaciones)

    context['Habitaciones'] = habitaciones

    # Fin combo Habitaciones

    # Combo Especialidades
    miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM clinico_Especialidades"
    curt.execute(comando)
    print(comando)

    especialidades = []
    especialidades.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        especialidades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(especialidades)

    context['Especialidades'] = especialidades

    # Fin combo Especialidades

    # Combo Medicos
    miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    curt = miConexiont.cursor()
    comando = "SELECT p.id id, p.nombre  nombre FROM planta_planta p ,  planta_perfilesplanta perf WHERE perf.sedesClinica_id = '" + str(
        Sede) + "' AND perf.tiposPlanta_id = 6 "

    curt.execute(comando)
    print(comando)

    medicos = []
    medicos.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        medicos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(medicos)

    context['Medicos'] = medicos
    context['Perfil'] = Perfil

    # Fin combo Medicos

    if (Perfil == 1):
        return render(request, "menuMedico.html", context)
    if (Perfil == 2):
        return render(request, "menuEnfermero.html", context)
    if (Perfil == 3):
        return render(request, "menuAuxiliar.html", context)
    if (Perfil == 4):
        return render(request, "citasMedicas/menuCitasMedicas.html", context)
    if (Perfil == 5):
        return render(request, "facturacion/menuFacturacion.html", context)
    if (Perfil == 6):
        print ("Entre por dende ERA")
        return render(request, "admisiones/panelHospAdmisionesBravo.html", context)

    return render(request, "admisiones/panelHospAdmisionesBravo.html", context)


def salir(request):
    print("Voy a Salir")

    miConexion = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM planta_tiposPlanta"
    cur.execute(comando)
    print(comando)

    perfiles = []
    context = {}

    for id, nombre in cur.fetchall():
        perfiles.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(perfiles)

    context['Perfiles'] = perfiles

    miConexion = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM sitios_sedesClinica"
    cur.execute(comando)
    print(comando)

    sedes = []

    for id, nombre in cur.fetchall():
        sedes.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(sedes)

    context['Sedes'] = sedes





    return render(request, "accesoPrincipal.html", context)



def validaPassword(request, username, contrasenaAnt,contrasenaNueva,contrasenaNueva2):
    print("Entre ValidaPassword" )
    username = request.POST["username"]
    contrasenaAnt = request.POST["contrasenaAnt"]
    contrasenaNueva = request.POST["contrasenaNueva"]
    contrasenaNueva2 = request.POST["contrasenaNueva2"]

    print(username)
    print(contrasenaAnt)
    print(contrasenaNueva)
    print(contrasenaNueva2)
    context = {}

    if (contrasenaNueva2 != contrasenaNueva):
        dato = "No coinciden las contraseñas ! "
        context['Error'] = "No coincideln las contraseñas ! "
        print(context)

        return HttpResponse(dato)


    miConexion1 = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    cur1 = miConexion1.cursor()
    comando = "SELECT documento,contrasena FROM planta_planta WHERE documento = '" + str(username) + "'"
    print(comando)
    cur1.execute(comando)

    UsuariosHc = []

    for documento, contrasena in cur1.fetchall():
        UsuariosHc = {'username': documento, 'contrasena': contrasena}

    miConexion1.close()
    print(UsuariosHc)

    if UsuariosHc == []:

        dato = "Personal invalido ! "
        context['Error'] = "Personal invalido ! "
        print(context)

        return HttpResponse(dato)
        #return render(request, "accesoPrincipal.html", context)

    else:
        miConexion1 = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
        cur1 = miConexion1.cursor()
        comando = "SELECT documento,contrasena FROM planta_planta WHERE documento = '" + str(username) + "' AND contrasena = '" + str(contrasenaAnt) + "'"
        print(comando)
        cur1.execute(comando)

        ContrasenaHc = []
        for documento, contrasena in cur1.fetchall():
            ContrasenaHc = {'username': documento, 'contrasena': contrasena}
        miConexion1.close()

        if ContrasenaHc == []:
            dato = "Contraseña Invalida ! "
            context['Error'] = "Contraseña Invalida ! "
            print(context)

            return HttpResponse(dato)

        else:

            miConexion1 = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
            cur1 = miConexion1.cursor()
            comando = "UPDATE planta_planta SET contrasena = '" +  str(contrasenaNueva) + "' WHERE documento = '" + str(username) + "'"
            print(comando)
            cur1.execute(comando)
            miConexion1.commit()
            miConexion1.close()
            context['Error'] = "Contraseña Actualizada ! "
            dato = "Contraseña Actualizada !"
            print(context)
            #return HttpResponse(context, safe=False)
            return HttpResponse(dato)
            #return render(request, "accesoPrincipal.html", context)


    #return JsonResponse(UsuariosHc, safe=False)

def Modal(request, username, password):

        print("Entre a Modal")
        print(username)
        print(password)

        miConexion1 = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
        cur1 = miConexion1.cursor()
        comando = "SELECT documento,contrasena FROM planta_planta WHERE documento = '" + str(username) + "'"
        print(comando)
        cur1.execute(comando)

        UsuariosHc = {}

        for documento, contrasena in cur1.fetchall():
            UsuariosHc = {'username': documento, 'contrasena': contrasena}

        miConexion1.close()
        print(UsuariosHc)
        return JsonResponse(UsuariosHc, safe=False)
        # return HttpResponse(UsuariosHc)


def admHospProvisional(request,Documento, Perfil,  Sede, Servicio):

    print("admHospProvisional")
    print(Documento)
    context1 = {}
    context1['Documento'] = Documento
    context1['Perfil'] = Perfil
    print (Perfil)
    context1['Sede'] = Sede
    print ("En admHospProvisional la sede = a ", Sede)
    print("En admHospProvisional la sede Context = a ", context1['Sede'] )
    #context1['NombreSede'] = NombreSede
    context1['Servicio'] = Servicio




    return render(request, "admisiones/panelHospAdmisiones.html", context1)



def buscarAdmision(request):
    context = {}


    print("Entre Buscar Admision" )
    BusHabitacion = request.POST["busHabitacion"]
    BusTipoDoc = request.POST["busTipoDoc"]
    BusDocumento = request.POST["busDocumento"]
    BusDesde = request.POST["busDesde"]
    BusHasta = request.POST["busHasta"]
    BusEspecialidad = request.POST["busEspecialidad"]
    BusMedico = request.POST["busMedico"]
    BusServicio = request.POST["busServicio"]
    BusPaciente = request.POST["busPaciente"]
    Perfil = request.POST['Perfil']

    Sede = request.POST["Sede"]
    print("Sede  = ", Sede)

    print("BusHabitacion= ", BusHabitacion)
    print("BusTipoDoc=", BusTipoDoc)
    print("BusDocumento=" , BusDocumento)
    print("BusDesde=", BusDesde)
    print("BusHasta=", BusHasta)
    print("La sede es = " , Sede)
    print("El busServicio = ", BusServicio)
    print("El busEspecialidad = ", BusEspecialidad)
    print("El busSMedico = ", BusMedico)
    print("El busSMedico = ", BusPaciente)

    ingresos = []

    # Combo de Servicios
    miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    curt = miConexiont.cursor()
    comando = "SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed.sedesClinica_id ='" + str(Sede) + "' AND sed.servicios_id = ser.id"
    curt.execute(comando)
    print(comando)

    servicios = []
    servicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        servicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(servicios)

    context['Servicios'] = servicios

    # Fin combo servicios

    # Combo TiposDOc
    miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM usuarios_TiposDocumento"
    curt.execute(comando)
    print(comando)

    tiposDoc = []
    tiposDoc.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposDoc.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposDoc)

    context['TiposDoc'] = tiposDoc

    # Fin combo TiposDOc


    # Combo Habitaciones
    miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM sitios_dependencias where sedesClinica_id = '" + str(Sede) +"' AND dependenciasTipo_id = 1"
    curt.execute(comando)
    print(comando)

    habitaciones = []
    habitaciones.append({'id': '', 'nombre': ''})


    for id, nombre in curt.fetchall():
        habitaciones.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(habitaciones)

    context['Habitaciones'] = habitaciones

    # Fin combo Habitaciones

    # Combo Especialidades
    miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM clinico_Especialidades"
    curt.execute(comando)
    print(comando)

    especialidades = []
    especialidades.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        especialidades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(especialidades)

    context['Especialidades'] = especialidades

    # Fin combo Especialidades

    # Combo Medicos
    miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    curt = miConexiont.cursor()
    comando = "SELECT p.id id, p.nombre  nombre FROM planta_planta p ,  planta_perfilesplanta perf WHERE perf.sedesClinica_id = '" + str(Sede) +"' AND perf.tiposPlanta_id = 6 "
    curt.execute(comando)
    print(comando)

    medicos = []
    medicos.append({'id': '', 'nombre': ''})


    for id, nombre in curt.fetchall():
        medicos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(medicos)

    context['Medicos'] = medicos

    # Fin combo Medicos


    # Busco Nombre de Habitacion

    miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    curt = miConexiont.cursor()
    comando = "SELECT d.id id, d.nombre  nombre FROM sitios_dependencias d WHERE d.id = '" + str(BusHabitacion) + "'"
    curt.execute(comando)
    print(comando)

    NombreHabitacion = ""


    for id, nombre in curt.fetchall():
        NombreHabitacion = nombre

    miConexiont.close()
    print("NombreHabitacion = ", NombreHabitacion)


    # Fin busco nombre de habitacion



    miConexion1 = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    cur1 = miConexion1.cursor()

 #   detalle = "SELECT i.tipoDoc_id tipoDoc, i.documento_id documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, serviciosIng_id,  dependenciasIngreso_id , dxIngreso_id FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep  WHERE i.sedesClinica_id = dep.sedesClinica_id AND i.dependenciasActual_id = dep.id AND i.sedesClinica_id = '" +    str(Sede) +"'"
  #  detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag  WHERE i.sedesClinica_id = dep.sedesClinica_id AND i.serviciosActual_id = dep.servicios_id AND i.serviciosActual_id = ser.id  AND i.dependenciasActual_id = dep.id AND  i.dependenciasIngreso_id = dep.id AND i.sedesClinica_id= '" + str(Sede) + "' AND dep.sedesClinica_id = i.sedesClinica_id AND i.sedesClinica_id = ser.sedesClinica_id AND deptip.id = dep.dependenciasTipo_id  AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id and diag.id = i.dxactual_id"
    detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd  WHERE sd.sedesClinica_id = i.sedesClinica_id  and   sd.servicios_id  = ser.id and   i.sedesClinica_id = dep.sedesClinica_id AND i.dependenciasActual_id = dep.id AND i.sedesClinica_id= '" + str(Sede) + "'  AND  deptip.id = dep.dependenciasTipo_id and dep.servicios_id = ser.id AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id and u.id = i.documento_id and diag.id = i.dxactual_id"


    print(detalle)

    if BusServicio != "":
      detalle = detalle + " AND  ser.id = '" + str(BusServicio) + "'"
    print(detalle)

    if BusDesde != "":
        detalle = detalle +  " AND i.fechaIngreso >= '" + str(BusDesde) +"'"
        print (detalle)

    if BusHasta != "":
        detalle = detalle + " AND i.fechaIngreso <=  '" + str(BusHasta) + "'"
        print(detalle)

    if BusHabitacion != "":
        detalle = detalle + " AND dep.id = '" + str(BusHabitacion) + "'"
        print(detalle)

    if BusTipoDoc != "":
            detalle = detalle + " AND i.tipoDoc_id= '" + str(BusTipoDoc) + "'"
            print(detalle)

    if BusDocumento != "":
                detalle = detalle + " AND u.documento= '" + str(BusDocumento) + "'"
                print(detalle)

    if BusPaciente != "":
        detalle = detalle + " AND u.nombre like '%" + str(BusPaciente) + "%'"
        print(detalle)

    if BusMedico != "":
        detalle = detalle + " AND i.medicoActual_id = '"  + str(BusMedico) + "'"
        print(detalle)

    cur1.execute(detalle)



    for tipoDoc, documento_id, nombre , consec, fechaIngreso,  fechaSalida, servicioNombreIng, camaNombreIng, dxActual  in cur1.fetchall():

        ingresos.append ({'tipoDoc' : tipoDoc, 'Documento': documento_id, 'Nombre': nombre , 'Consec': consec, 'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida, 'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng, 'DxActual': dxActual})

    miConexion1.close()
    print(ingresos)
    context['Ingresos'] = ingresos




    return render(request, "admisiones/panelHospAdmisionesBravo.html", context)



def buscarHabitaciones(request):
    context = {}
    Serv = request.GET["Serv"]
    Sede = request.GET["Sede"]
    print ("Entre buscar habitaciones servicio =",Serv)
    print ("Sede = ", Sede)


    # Busco la habitaciones de un Servicio

    miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
    curt = miConexiont.cursor()
    comando = "SELECT d.id id, d.numero  nombre FROM sitios_dependencias d , sitios_serviciossedes ser WHERE d.sedesclinica_id = ser.sedesclinica_id and d.sedesclinica_id = '" + str(Sede) + "' and  d.dependenciastipo_id=2 and  d.servicios_id = ser.id and ser.servicios_id='" + str(Serv.lstrip()) + "' "
    curt.execute(comando)
    print(comando)

    Habitaciones =[]


    for id, nombre in curt.fetchall():
        Habitaciones.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(Habitaciones)
    context['Habitaciones'] = Habitaciones

    context['Sede'] = Sede



    return JsonResponse(json.dumps(Habitaciones), safe=False)

def guardarAdmision(request):
    print("Entre a guardar Admision")
    context = {}
    Sede = request.POST["Sede"]
    Servicio = request.POST["Servicio"]
    Perfil = request.POST["Perfil"]
    Username = request.POST["Username"]
    print ("Sede = ", Sede)
    print("Servicio = ", Servicio)
    print("Perfil = ", Perfil)
    print("Username = ", Username)

    sedesClinica = request.POST['sedesClinica']
    tipoDoc = request.POST['tipoDoc']
    documento = request.POST['documento']
    consec = request.POST['consec']
    fechaIngreso = request.POST['fechaIngreso']
    fechaSalida = request.POST['fechaSalida']
    factura = request.POST['factura']
    numcita = request.POST['numcita']
    dependenciasIngreso = request.POST['dependenciasIngreso']
    dependenciasActual = request.POST['dependenciasActual']
    dependenciasSalida = request.POST['dependenciasSalida']
    dxIngreso = request.POST['dxIngreso']
    dxActual = request.POST['dxActual']
    dxSalida = request.POST['dxSalida']
    estadoSalida = request.POST['estadoSalida']
    medicoIngreso = request.POST['medicoIngreso']
    medicoActual = request.POST['medicoActual']
    medicoSalida = request.POST['medicoSalida']
    salidaDefinitiva = request.POST['salidaDefinitiva']
    usuarioRegistro = Username
    fechaRegistro = request.POST['fechaRegistro']
    estadoRegistro = "A"
    print ("Pase parte dura de Guardar Admision. AHora si a guardar")


class crearAdmision(TemplateView):
    print("Entre a Craer Admision")

    template_name = 'admisiones/crearAdmision.html'
    print("Entre a Registrar Admision")

    def post(self, request, *args, **kwargs):
        print("Entre POST de Crear Admisiones")
        data = {}
        context = {}
        #sedesClinica = request.POST['sedesClinica']
        sedesClinica = request.POST['Sede']
        Sede = request.POST['Sede']
        context['Sede'] = Sede
        Perfil = request.POST['Perfil']
        context['Perfil'] = Perfil


        print("Sedes Clinica = ", sedesClinica)
        print ("Sede = ",Sede)


        Username = request.POST["Username"]
        print(" = " , Username)
        context['Username'] = Username

        Username_id = request.POST["Username_id"]
        print("Username_id = ", Username_id)
        context['Username_id'] = Username_id



        tipoDoc = request.POST['tipoDoc']
        documento = request.POST['documento']
        print("tipoDoc = ", tipoDoc)
        print("documento = ", documento)
        #extraServicio = request.POST['extraServicio']
       #print("extraServicio = ", extraServicio)

        consec = Ingresos.objects.all().filter(documento_id = documento).aggregate(Max('consec'))
        print("consecutivo Inicial =", consec)
        consecutivo1 = consec['consec__max']
        consecutivo = consec['consec__max']

        if consecutivo1 == None:
            consecutivo = 1
        else:
            consecutivo = consecutivo + int(1)



        print("consecutivo =", consecutivo)
        consec = consecutivo
        fechaIngreso = request.POST['fechaIngreso']
        print("fechaIngreso =", fechaIngreso)
        fechaSalida = "0001-01-01 00:00:00"

        factura = 0
        numcita = 0
        dependenciasIngreso = request.POST['dependenciasIngreso']
        print("dependenciasIngreso =", dependenciasIngreso)
        dependenciasActual = dependenciasIngreso
        dependenciasSalida = ""
        dxIngreso = request.POST['dxIngreso']
        print("dxIngreso =", dxIngreso)
        dxActual = dxIngreso
        dxSalida = ""
        estadoSalida = "1"

        medicoIngreso = request.POST['medicoIngreso']
        print("medicoIngreso =", medicoIngreso)
        medicoActual = medicoIngreso
        medicoSalida = ""
        salidaClinica = "N"
        salidaDefinitiva = "N"

        usuarioRegistro = Username_id

        print("usuarioRegistro =", usuarioRegistro)
        now = datetime.now()
        dnow=now.strftime("%Y-%m-%d %H:%M:%S")
        print ("NOW  = ", dnow)

        fechaRegistro = dnow
        estadoReg = "A"
        print("estadoRegistro =", estadoReg)

        data[0] = "Ha ocurrido un error"

        # VAmos a guardar la Admision

        grabo = Ingresos(
                         sedesClinica_id=Sede,
                         tipoDoc_id=tipoDoc,
                         documento_id=documento,
                         consec=consec,
                         fechaIngreso=fechaIngreso,
                         fechaSalida=fechaSalida,
                         factura=factura,
                         numcita=numcita,
                         dependenciasIngreso_id=dependenciasIngreso,
                         dxIngreso_id=dxIngreso,
                         medicoIngreso_id=medicoIngreso,
                         dependenciasActual_id=dependenciasActual,
                         dxActual_id = dxActual,
                         medicoActual_id=medicoActual,
                         dependenciasSalida_id = dependenciasSalida,
                         dxSalida_id = dxSalida,
                         medicoSalida_id=medicoSalida,
                         estadoSalida_id = estadoSalida,

                         salidaClinica = salidaClinica,
                         salidaDefinitiva=salidaDefinitiva,
                         fechaRegistro=fechaRegistro,
                         usuarioRegistro_id=usuarioRegistro,
                         estadoReg=estadoReg

        )
        print("Voy a fiu¿guardar la INFO")


        grabo.save()
        print("yA grabe 2", grabo.id)
        grabo.id
        print("yA grabe" , grabo.id)

       # RUTINA ARMADO CONTEXT

        ingresos = []

        miConexionx = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
        curx = miConexionx.cursor()


        detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag  , sitios_serviciosSedes sd WHERE  sd.sedesClinica_id = i.sedesClinica_id  and   sd.servicios_id  = ser.id and   i.sedesClinica_id = dep.sedesClinica_id AND i.dependenciasActual_id = dep.id AND i.sedesClinica_id= '" + str(
            Sede) + "'  AND  deptip.id = dep.dependenciasTipo_id and dep.servicios_id = ser.id AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id and u.id = i.documento_id and diag.id = i.dxactual_id"
        print(detalle)

        curx.execute(detalle)

        for tipoDoc, documento, nombre, consec, fechaIngreso, fechaSalida, servicioNombreIng, camaNombreIng, dxActual in curx.fetchall():
            ingresos.append({'tipoDoc': tipoDoc, 'Documento': documento, 'Nombre': nombre, 'Consec': consec,
                             'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida,
                             'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                             'DxActual': dxActual})

        miConexionx.close()
        print(ingresos)
        context['Ingresos'] = ingresos

        # Combo de Servicios
        miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
        curt = miConexiont.cursor()
        comando = "SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed.sedesClinica_id ='" + str(Sede) + "' AND sed.servicios_id = ser.id"
        curt.execute(comando)
        print(comando)

        servicios = []
        servicios.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            servicios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(servicios)

        context['Servicios'] = servicios

        # Fin combo servicios

        # Combo TiposDOc
        miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
        curt = miConexiont.cursor()
        comando = "SELECT id ,nombre FROM usuarios_TiposDocumento "
        curt.execute(comando)
        print(comando)

        tiposDoc = []
        tiposDoc.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tiposDoc.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposDoc)

        context['TiposDoc'] = tiposDoc

        # Fin combo TiposDOc

        # Combo Habitaciones
        miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
        curt = miConexiont.cursor()
        comando = "SELECT id ,nombre FROM sitios_dependencias where sedesClinica_id = '" + str(
            Sede) + "' AND dependenciasTipo_id = 1"
        curt.execute(comando)
        print(comando)

        habitaciones = []

        for id, nombre in curt.fetchall():
            habitaciones.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(habitaciones)

        context['Habitaciones'] = habitaciones

        # Fin combo Habitaciones

        # Combo Especialidades
        miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
        curt = miConexiont.cursor()
        comando = "SELECT id ,nombre FROM clinico_Especialidades"
        curt.execute(comando)
        print(comando)

        especialidades = []
        especialidades.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            especialidades.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(especialidades)

        context['Especialidades'] = especialidades

        # Fin combo Especialidades

        # Combo Medicos
        miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
        curt = miConexiont.cursor()
        comando = "SELECT p.id id, p.nombre  nombre FROM planta_planta p ,  planta_perfilesplanta perf WHERE perf.sedesClinica_id = '" + str(
            Sede) + "' AND perf.tiposPlanta_id = 6 "

        curt.execute(comando)
        print(comando)

        medicos = []
        medicos.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            medicos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(medicos)

        context['Medicos'] = medicos

        # Fin combo Medicos

        # FIN RUTINA ARMADO CONTEXT


        return render(request, "admisiones/panelHospAdmisionesBravo.html", context)



        return HttpResponse(json.dumps(data))

    def get_context_data(self,  **kwargs):
        print("Entre a Contexto")



        context = super().get_context_data(**kwargs)
        print(context['Sede'])
        Sede = context['Sede']


        # Combo de Servicios
        miConexiont = MySQLdb.connect(host='192.168.0.14', user='root', passwd='', db='vulnerable5')
        curt = miConexiont.cursor()
        comando = "SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed.sedesClinica_id ='" + str(Sede) + "' AND sed.servicios_id = ser.id"
        curt.execute(comando)
        print(comando)

        servicios = []
        servicios.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            servicios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(servicios)

        context['Servicios'] = servicios

        # Fin combo servicios


        context['title'] = 'Mi gran Template'
        context['form'] = crearAdmisionForm


   #     context['form2'] = historiaExamenesForm
        print("Se supone voya a cargar la forma")
        print (context)
        return context


def crearResponsables(request):
    print("Entre crear Responsables")
    pass