console.log('Hola Alberto Hi!')

var datavta;
var seriali = new Array();
var seriali1 = new Array();
var envio = new FormData()
var envio1 = new FormData()
var envio2 = new FormData()
var formData = new FormData()
var envio_final = new FormData()
var envio_final1 = new FormData()

var x=0
var  folio_final =0

const form = document.getElementById('formHistoria')

const form2 = document.getElementById('formClinicos')
console.log(form)
console.log(form2)




$(document).on('change', '#busServicio', function(event) {


        var Serv =   $("#busServicio option:selected").text();

        var Sede =  document.getElementById("Sede").value;

        $.ajax({
	           url: '/buscarHabitaciones',
	            data : {Serv:Serv, Sede:Sede},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);


                     const $id2 = document.querySelector("#busHabitacion");


 	      		     $("#busHabitacion").empty();


	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });



                    },
	   		    error: function (request, status, error) {

	   			    $("#mensajes").html(" !  Reproduccion  con error !");
	   	    	}

	     });
});




$(document).on('change', '#extraServicio_id', function(event) {

        alert("Entre Servicio Extra");
        var Serv =   $("#busServicio option:selected").text();

        var Sede =  document.getElementById("Sede").value;

        $.ajax({
	           url: '/buscarHabitaciones',
	            data : {Serv:Serv, Sede:Sede},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);


                     const $id2 = document.querySelector("#busHabitacion");


 	      		     $("#busHabitacion").empty();


	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });



                    },
	   		    error: function (request, status, error) {

	   			    $("#mensajes").html(" !  Reproduccion  con error !");
	   	    	}

	     });
});







// Para la ventana Moddal

 $('.eBtn').on('click',function(event)
	        {
			event.preventDefault();
			var href = $(this).attr('href');
			console.log("Entre Ventana Modal");

			$.get(href, function(UsuariosHc,status)
			 {
			 alert("entre");


                $('#username').val(UsuariosHc.username);
				$('#password').val(UsuariosHc.password);

				}
			);

			 $('#exampleModal').modal({show:true});

			  });



form.addEventListener('submit', e=>{

        e.preventDefault()


        var folio_oculto =  document.getElementById("folio_oculto").value

        if (folio_oculto != 0)
           {
             var id_tipo_doc    =  document.formHistoria["id_id_tipo_doc"].value
             var documento      =  document.formHistoria["id_documento"].value
             var folio  = ""
             var fecha          =  document.formHistoria["fecha"].value
             var estado_folio   =  document.formHistoria['id_estado_folio'].value
             var id_especialidad = document.formHistoria['id_id_especialidad'].value
             var id_medico =       document.formHistoria['id_id_medico'].value
             var motivo =          document.formHistoria['id_motivo'].value
             var subjetivo =       document.formHistoria['id_subjetivo'].value
             var objetivo =       document.formHistoria['id_objetivo'].value
             var analisis =        document.formHistoria['id_analisis'].value
             var plan =            document.formHistoria['id_plan'].value


               envio1.append('id_tipo_doc', id_tipo_doc );
               envio1.append( 'documento', documento);
               envio1.append('folio', document.getElementById("folio_oculto").value);
               envio1.append('fecha', fecha);
               envio1.append('id_especialidad' , id_especialidad);
               envio1.append('id_medico' , id_medico);
               envio1.append('motivo' , motivo);
               envio1.append('subjetivo' , subjetivo);
               envio1.append('objetivo' , objetivo);
               envio1.append('analisis' , analisis);
               envio1.append('plan' , plan);
               envio1.append('estado_folio' , estado_folio);





         // La Historia Clinica


         //       for (var valores in envio1.values) {
            //            alert(valores);
          //      }


               $.ajax({
            	   type: 'POST',
 	               url: '/historia1View/',
  	               data: envio1,
 	      		success: function (respuesta2) {
 	      		        var data = JSON.parse(respuesta2);

 	      	 			$("#mensajes").html("Registro de Historia Exitoso ");
 	      	 	          document.formHistoria["id_id_tipo_doc"].value ="";
                          document.formHistoria["id_documento"].value = "";
                          document.formHistoria["id_folio"].value = "";
                          document.formHistoria["fecha"].value = "";
                          document.formHistoria['id_estado_folio'].value = "";
                          document.formHistoria['id_id_especialidad'].value = "";
                          document.formHistoria['id_id_medico'].value = "";
                         document.formHistoria['id_motivo'].value = "";
                         document.formHistoria['id_subjetivo'].value = "";
                         document.formHistoria['id_objetivo'].value = "";
                         document.formHistoria['id_analisis'].value = "";
                        document.formHistoria['id_plan'].value = "";
                        alert ("me voy para el ultim ajax");


 	      		},
 	      		error: function (request, status, error) {
 	      			alert(request.responseText);
 	      			alert (error);
 	      			$("#mensajes").html("Error Venta AJAX O RESPUESTA");
 	      		},
 	      		cache : false,
 	      		contentType : false,
 	      		processData: false,

 	        });

            var nuevo={};
            var a=0;
            var conteo=0;

	 //for (var i=0; i <= seriali1.length; i++)
	for (var i=0; i < 1; i++)
			{

            alert(JSON.stringify(seriali1));

         for (var clave in seriali1){
                    // Controlando que json realmente tenga esa propiedad
                if (seriali1.hasOwnProperty(clave)) {
                 // Mostrando en pantalla la clave junto a su valor
                      alert("La clave es " + clave+ " y el valor es " + seriali1[clave]);
                      envio_final = seriali1[clave];


                     }
                    }
                  //  formData = JSON.stringify(formData);

                    console.log("Van los FormDatas");
                    alert("Longitud envio_final");
                    alert(envio_final.length);

                   // Display the key/value pairs
                    for(var pair of envio_final.entries()) {
                    console.log(pair[0]+ ', '+ pair[1]);
                    envio_final1.append(pair[0], pair[1])
                    conteo=conteo +1;
                    if (conteo == 8 || conteo==16 || conteo==24  || conteo==32)
                        {
                         // inserto desde aqui
                            alert("entre conteo");


	    	$.ajax({
            	   type: 'POST',
 	               url: '/historiaExamenesView/',
  	               data: envio_final1,
 	      		success: function (respuesta2) {
 	      	 				$("#mensajes").html("Examenes Creados " + respuesta2);

 	      			       var trs=$("#Examenes tr").length;
                            if(trs>1)
                                    {
                               // Eliminamos la ultima columna
                                    $("#Examenes td").remove();
                                    }
                          document.formHistoria["id_id_tipo_doc"].value ="";
                          document.formHistoria["id_documento"].value = "";
                          document.formHistoria["id_folio"].value = "";
                          document.formHistoria["fecha"].value = "";
                          document.formHistoria['id_estado_folio'].value = "";
                          document.formHistoria['id_id_especialidad'].value = "";
                          document.formHistoria['id_id_medico'].value = "";
                         document.formHistoria['id_motivo'].value = "";
                         document.formHistoria['id_subjetivo'].value = "";
                         document.formHistoria['id_objetivo'].value = "";
                         document.formHistoria['id_analisis'].value = "";
                        document.formHistoria['id_plan'].value = "";

                          		envio_final1.delete('id_tipo_doc');
	                	envio_final1.delete('documento');
	                    envio_final1.delete('folio');
	                 	envio_final1.delete('fecha');
	                	envio_final1.delete('id_TipoExamen');
	                	envio_final1.delete('id_examen');
	                	envio_final1.delete('cantidad');
	                	envio_final1.delete('estado_folio');


 	      		},
 	      		error: function (request, status, error) {
 	      			alert(request.responseText);
 	      			alert (error);
 	      			$("#mensajes").html("Error Venta AJAX O RESPUESTA");
 	      		},
 	      		cache : false,
 	      		contentType : false,
 	      		processData: false,

 	              });





                      /// termino inserto desde aqui



                        }




                    }




          } // Cierra For
       }  // Cierra If positivo
        else
        {
        $("#mensajes").html(" ! Favor Primero Conseguir Nro De Folio antes de Enviar  ¡");
        }

})


$("#btnFolio").click(function(){

// El Tema del Folio
             var id_tipo_doc    =  document.formHistoria["id_id_tipo_doc"].value
             var documento      =  document.formHistoria["id_documento"].value

                  envio2.append('id_tipo_doc', id_tipo_doc );
                  envio2.append( 'documento', documento);

             	$.ajax({
            	   type: 'POST',
 	               url: '/consecutivo_folios/',
  	               data: envio2 ,
 	      		success: function (respuesta2) {
 	      		             var data = JSON.parse(respuesta2);
 	      		              alert("folio Ultiomop es ");
 	      		            alert(data.ultimofolio)
 	      	 				document.getElementById("folio_oculto").value= data.ultimofolio;
 	      	 			//	document.getElementById("id_folio").value= data.ultimofolio;

 	      			      		},
 	      		error: function (request, status, error) {
 	      			alert(request.responseText);
 	      			alert (error);
 	      			$("#mensajes").html("Error Venta AJAX O RESPUESTA");
 	      		},
 	      		cache : false,
 	      		contentType : false,
 	      		processData: false,

 	        });
});


