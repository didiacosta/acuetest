function MicrocourseViewModel() {
	var self = this;
	self.listado = ko.observableArray([]);
	self.mensaje = ko.observable('');

	self.consultar = function(){
		path = path_principal + '/api/microcourse/list/?format=json';
		parameter = {}
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
	
	}
}

var microcourse = new MicrocourseViewModel();
ko.applyBindings(microcourse);
