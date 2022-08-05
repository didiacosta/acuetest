function MicrocourseViewModel() {
	var self = this;
	self.listado = ko.observableArray([]);
	self.mensaje = ko.observable('');

	self.myVO = {
		email: ko.observable('').extend({ 
			required: { message: 'The email address is required.' },
			email: {message: 'Email addres is not valid'} 
		})
	}
	self.getData = function(order,descending, obj){
		path = path_principal + '/api/microcourse/list/?format=json';
		parameter = {
			order: order,
			descending: descending
		}

		RequestGet(function (datos, success, mensage) {
		 	if (success == 'success' && datos!=null && datos.length > 0) {
		 		self.mensaje('');
		 		self.listado(agregarOpcionesObservable(datos));
		 	} else {
		 		self.listado([]);
		 		self.mensaje(mensajeNoFound);
		 	}
		 	cerrarLoading();
		},path, parameter,undefined, false);

		$('.order').attr("style","color: #858796; cursor:pointer");	
		$('#'+obj).attr("style","color: blue; cursor: pointer");
		
	}
	self.showModal = function(){
		$('#ModalSendReport').modal('show');
	}
	self.sendReport = function() {
		if (MicrocourseViewModel.myErrors().length == 0) {
			var parametros={
				callback:function(datos, success, mensaje){

					if (success=='success') {
						$('#ModalSendReport').modal('hide');
					}else{
						 mensajeError(mensaje);
					}
				}, //funcion para recibir la respuesta 
				url:path_principal+'/api/microcourse/emailreport/',//url api
				parametros:self.myVO,
				alerta:true,
				metodo: 'POST'
			};
			RequestFormData(parametros);
		}else{
			MicrocourseViewModel.myErrors.showAllMessages();
		}
	}
}

var microcourse = new MicrocourseViewModel();
MicrocourseViewModel.myErrors = ko.validation.group(microcourse.myVO);
ko.applyBindings(microcourse);
