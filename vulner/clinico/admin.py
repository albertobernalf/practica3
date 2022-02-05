from django.contrib import admin

# Register your models here.

from clinico.models import Medicos, Especialidades , TiposExamen, Examenes, Historia, HistoriaExamenes, HistoriaResultados, EspecialidadesMedicos, Servicios, Diagnosticos, EstadosSalida


class especialidadesAdmin(admin.ModelAdmin):

        list_display = ("id", "nombre")
        search_fields = ("id", "nombre")


#class medicosAdmin(admin.ModelAdmin):

#    list_display = ("id","nombre","direccion","telefono","contacto")
#    search_fields = ("id","nombre","direccion","telefono","contacto")

class tiposExamenAdmin(admin.ModelAdmin):
        list_display = ("id", "nombre")
        search_fields = ("id", "nombre")

class examenesAdmin(admin.ModelAdmin):

    list_display = ("id","nombre","id_TipoExamen")
    search_fields = ("id","nombre","id_TipoExamen")


class historiaExamenesAdmin(admin.ModelAdmin):
    fields = ('id_TipoExamen', 'id_examen', 'cantidad',)
    list_display = ("id", "id_tipo_doc", "documento", "folio", "fecha", "id_TipoExamen", "id_examen")
    search_fields = ("id", "id_tipo_doc", "documento", "folio", "fecha", "id_TipoExamen", "id_examen")


class historiaAdmin(admin.ModelAdmin):

        list_display = ("id", "id_tipo_doc", "documento","folio","fecha","motivo")
        search_fields = ("id", "id_tipo_doc", "documento","folio","fecha","motivo")




class historiaResultadosAdmin(admin.ModelAdmin):
    list_display = ("id", "id_tipo_doc", "documento", "folio", "fecha", "consecutivo","id_TipoExamen", "id_examen","resultado")
    search_fields =  ("id", "id_tipo_doc", "documento", "folio", "fecha", "consecutivo","id_TipoExamen", "id_examen","resultado")

class serviciosAdmin(admin.ModelAdmin):
        list_display = ("id", "nombre")
        search_fields = ("id", "nombre")


class serviciosAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")

class especialidadesMedicosAdmin(admin.ModelAdmin):
        list_display = ("id", "id_especialidad", "id_medico")
        search_fields = ("id", "id_especialidad", "id_medico")

class diagnosticosAdmin(admin.ModelAdmin):
            list_display = ("id", "nombre")
            search_fields = ("id", "nombre")


class estadosSalidaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")



#admin.site.register(Medicos, medicosAdmin)
admin.site.register(Especialidades, especialidadesAdmin)
admin.site.register(TiposExamen, tiposExamenAdmin)
admin.site.register(Examenes, examenesAdmin)
admin.site.register(Historia, historiaAdmin)
admin.site.register(HistoriaExamenes, historiaExamenesAdmin)
admin.site.register(HistoriaResultados, historiaResultadosAdmin)
admin.site.register(Servicios, serviciosAdmin)
admin.site.register(EspecialidadesMedicos, especialidadesMedicosAdmin)
admin.site.register(Diagnosticos, diagnosticosAdmin)
admin.site.register(EstadosSalida, estadosSalidaAdmin)


