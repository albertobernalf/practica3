import json
from django import forms
import cv2
import numpy as np
#import onnx as onnx
#import onnxruntime as ort
import pyttsx3
import speech_recognition as sr


from django.db.models.functions import Cast, Coalesce
from django.utils.timezone import now
from django.db.models import Avg, Max, Min
from .forms import historiaForm, historiaExamenesForm

from clinico.models import Historia, HistoriaExamenes, Examenes, TiposExamen, EspecialidadesMedicos, Medicos
from usuarios.models import Usuarios, TiposDocumento

from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.core.exceptions import ValidationError
from django.urls import reverse, reverse_lazy
# from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView
from django.http import JsonResponse

# Create your views here.


def prueba(request):
    return render(request, "index.html")

def resMotivoInvidente(request):
    print("Entre a Reconocer audio Motivo Consulta")
    r = sr.Recognizer()
    print(sr.Microphone.list_microphone_names())

    with sr.Microphone(device_index=0) as source:  # use the default microphone as the audio source
        print("Por Favor cuenteme :")

        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)  # listen for the first phrase and extract it into audio data
        print("pase")
    try:
        print("No haga nada")
        # print("You said " + r.recognize_google(audio , language = 'en-IN', show_all = True))  # recognize speech using Google Speech Recognition
        # text = r.recognize_google(audio, language = 'es-CO', show_all = True )
        text = r.recognize_google(audio, language='es-CO', show_all=True)
      #  jsonToPython = json.loads(format(text))
        print('You said: {}'.format(text))


    except LookupError:  # speech is unintelligible
        print("Could not understand audio")

     # return render(request, "home.html")

    datos = {"Respuesta": format(text)}
    print(datos)

    return HttpResponse(json.dumps(datos))




def motivoInvidente(request):
    print("Entre al Moivo invidente Audio")
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    texto = request.GET["nombre"]
    engine.say(texto)
    engine.runAndWait()

    return redirect('/menu/')


def buscaExamenes(request):
    print("Entre a Buscar Examenes Clinicos")

    id = request.GET.get('id')
    print (id)



    datos = {"id": id}
    print(datos)

    return  HttpResponse(json.dumps(datos))

def consecutivo_folios(request):

    print ("Entre a Consecutivo_folios")
    id_tipo_doc =  request.POST["id_tipo_doc"]
    documento = request.POST["documento"]

    id_tipo_doc1 = TiposDocumento.objects.get(id=id_tipo_doc)

    ultimofolio = Historia.objects.all().filter(id_tipo_doc=id_tipo_doc1.id).filter(documento=documento).aggregate(maximo = Coalesce(Max('folio'), 0))
    ultimofolio2= (ultimofolio['maximo'] + 1)

    datos = {"ultimofolio": ultimofolio2}
    print(datos)

    return HttpResponse(json.dumps(datos))


def historiaExamenesView(request):
    print("Entre por historiaExamenesView")
    form2 = historiaExamenesForm(request.POST or None)
    print("Esta es form2")
    print(form2)
    data = {}
    if request.is_ajax():
        if form2.is_valid():
            print("Entere a Grabar")
            form2.save()
            data['Nombre'] = form2.cleaned_data.get('documento')
    context = {'form2': form2}

    # return redirect('/menu/')
    # return render(request, 'historia_form.html', context)
    return HttpResponse(data)


def historia1View(request):
    print("Entre Ajax de Historia1View")

    form = historiaForm(request.POST)
    print(form)
    data1 = {}
    if request.is_ajax():
        print("Entre Ajax Historia a validadr Form")
        if form.is_valid():
            print("Entre a Grabar Ajax Historia")
            form.save()
            data1 ={'Nombre', form.cleaned_data.get('documento')}

            return HttpResponse(data1)
        else:
            print("Formulario Ajax invalido")
            return HttpResponse("Formulario Ajax invalido")
    return HttpResponse("Problemas con AJAx")


def historiaView(request):
    print("Entre por el view historiaView")

    form = historiaForm(request.POST)

    if request.method == 'POST':
        print("entre por POST")

        # Check if the form is valid:
        if form.is_valid():
            form1 = form.cleaned_data
            print("A grabar")

            grabo = Historia(id_tipo_doc=form1['id_tipo_doc'],
                             documento=form1['documento'],
                             folio=form1['folio'],
                             fecha=form1['fecha'],
                             id_especialidad=form1['id_especialidad'],
                             id_medico=form1['id_medico'],
                             motivo=form1['motivo'],
                             subjetivo=form1['subjetivo'],
                             objetivo=form1['objetivo'],
                             analisis=form1['analisis'],
                             plan=form1['plan'],
                             estado_folio=form1['estado_folio'])
            grabo.save()
            grabo.id
            print("yA grabe")

            messages.success(request, 'Informacion guardada')

            return redirect('/historiaView')
        else:
            print("Error")
            print(form.errors)
            messages.error(request, form.errors['documento'])

    else:
        print("pase por el else")

        form = historiaForm()
        form2 = historiaExamenesForm()

        return render(request, 'historia_form.html', {'form': form, 'form2': form2})

    form2 = historiaExamenesForm()
    return render(request, 'historia_form.html', {'form': form, 'form2': form2})


def motivoSeñas(request):
    print("Entre Reproduce SeÃ±as")
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)

    texto = step_5_camera()
    print("De devuelta el texto es : ")
    print(texto)

    #  texto = request.GET["nombre"]
    engine.say(texto)
    engine.runAndWait()

    datos = {"mensaje": texto}
    print(datos)

    return HttpResponse(json.dumps(datos))

    return redirect('/menu/')


def subjetivoSeñas(request):
    print("Entre Reproduce SubjetivoSeñas")
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)

    texto = step_5_camera()
    print("De devuelta el texto es : ")
    print(texto)

    #  texto = request.GET["nombre"]
    engine.say(texto)
    engine.runAndWait()

    datos = {"mensaje": texto}
    print(datos)

    return HttpResponse(json.dumps(datos))

    return redirect('/menu/')


def step_5_camera():
    print("Entree a Camara")
    onnx_file = 'C:\\EntornosPython\\vulne\\vulnerable\\signlanguage.onnx'
    onnx_model = onnx.load(onnx_file)
    onnx.checker.check_model(onnx_model)
    print('The model is checked!')

    # constants
    index_to_letter = list('ABCDEFGHIKLMNOPQRSTUVWXY')
    mean = 0.485 * 255.
    std = 0.229 * 255.
    print("Adentro1")
    # create runnable session with exported model
    ort_session = ort.InferenceSession(onnx_file)
    print("Adentro11")
    cap = cv2.VideoCapture(0)
    mensaje = []
    print("Adentro2")

    # while True:
    for t in range(15):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # preprocess data
        frame = center_crop(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        x = cv2.resize(frame, (28, 28))
        x = (x - mean) / std

        x = x.reshape(1, 1, 28, 28).astype(np.float32)
        y = ort_session.run(None, {'input': x})[0]

        index = np.argmax(y, axis=1)
        letter = index_to_letter[int(index)]

        mensaje.append(letter)
        print("las letras son: %s", mensaje)

        cv2.putText(frame, letter, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), thickness=2)
        cv2.imshow("Sign Language Translator", frame)
        print("Adentro3")
        #  if cv2.waitKey(1) & 0xFF == ord('q'):
        #  break

    # cv2.waitKey(0)
    cv2.destroyAllWindows()
    cap.release()

    print("El mensaje Final es : ")

    resultado = ''

    for x in range(0, len(mensaje)):
        resultado = resultado + mensaje[x]

    return (resultado)


def center_crop(frame):
    h, w, _ = frame.shape
    start = abs(h - w) // 2
    if h > w:
        return frame[start: start + w]
    return frame[:, start: start + h]


class nuevoView(TemplateView):
    print("Encontre")
    template_name = 'historia_form.html'

    def post(self, request, *args, **kwargs):
        print("Entre POST")
        data = {}
        try:
            print("Entre try")
            if 'action' in request.POST:
                action = request.POST['action']
                id = request.POST['id']
            else:
                print ("Falsa action")
                action = False
            print(action)
            print(id)
           
            action = request.POST.get('action', False)

            if action == 'BuscaExamenes':
                print("Entre Action")
                data = []
                for s in Examenes.objects.all().filter(id_TipoExamen=request.POST["id"]):
                      data.append({'id': s.id, 'nombre': s.nombre})
                      print (data[0])
            else:
              data[0] = "Ha ocurrido un error"

            if action == 'BuscaEspecialidad':
                  print("Entre Action especialidad")
                  print (id)
                  data = []
                  for s in EspecialidadesMedicos.objects.all().filter(id_especialidad=request.POST["id"]):
                      medico = Medicos.objects.get(nombre=s.id_medico)

                      data.append({'id': s.id, 'nombre': medico.nombre})
                      print(data[0])
            else:
                  data[0] = "Ha ocurrido un error"

        except Exception as  e:
              print ("Exception")
              data[0] = atrr(e)

        print("me devuelvo con ")

        return HttpResponse(json.dumps(data))

       # return JsonResponse(data, safe=False)

    def get_context_data(self, documento, **kwargs):
        print("Entre a Contexto")
        print (documento)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mi gran Template'
        context['form']  = historiaForm
        context['form2'] = historiaExamenesForm
        return context
