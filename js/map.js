var mymap = L.map('mapid', {
	center: [-23.6824, -46.5957],
	zoom: 10
});

var overlayMaps = {};
var furtosCelular	= L.markerClusterGroup();
var furtosVeiculo	= L.markerClusterGroup();
var homicidios		= L.markerClusterGroup();
var latrocinios		= L.markerClusterGroup();
var lesaoMorte		= L.markerClusterGroup();
var mortesPolicial	= L.markerClusterGroup();
var roubosCelular	= L.markerClusterGroup();
var roubosVeiculo	= L.markerClusterGroup();

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
	maxZoom: 18,
	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
	'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
	'Imagery © <a href="http://mapbox.com">Mapbox</a>',
	id: 'mapbox.streets'
}).addTo(mymap);

function eachLayer(layer) {
	var feature = layer.toGeoJSON();
	if (feature.properties && feature.properties.tipo) {
		text = "<p><strong>" + feature.properties.tipo + "</strong></p>";
		text += "<p><strong>Data:</strong> " + feature.properties.data_ocorrencia + "</p>";
		text += "<p><strong>Endereco:</strong> " + feature.properties.endereco + "</p>";
		layer.bindPopup(text);
	}
	// Related doc: http://leafletjs.com/reference-1.1.0.html#icon
	if(feature.properties.tipo == "Furto de Celular") {
		layer.options.icon = L.icon({
			iconUrl: "./img/furto.png",
			iconSize: [28, 45]
		});
		furtosCelular.addLayer(layer);
	} else if(feature.properties.tipo == "Furto de Veículo") {
		layer.options.icon = L.icon({
			iconUrl: "./img/furtoveiculo.png",
			iconSize: [28, 45]
		});
		furtosVeiculo.addLayer(layer);
	} else if(feature.properties.tipo == "Homicídio") {
		layer.options.icon = L.icon({
			iconUrl: "./img/homicidio.png",
			iconSize: [28, 45]
		});
		homicidios.addLayer(layer);
	} else if(feature.properties.tipo == "Latrocínio") {
		layer.options.icon = L.icon({
			iconUrl: "./img/latrocinio.jpg",
			iconSize: [28, 45]
		});
		latrocinios.addLayer(layer);
	} else if(feature.properties.tipo == "Lesão Seguida de Morte") {
		layer.options.icon = L.icon({
			iconUrl: "./img/lesaomorte.png",
			iconSize: [28, 45]
		});
		lesaoMorte.addLayer(layer);
	} else if(feature.properties.tipo == "Morte por Intervenção Policial") {
		layer.options.icon = L.icon({
			iconUrl: "./img/mortepolicial.png",
			iconSize: [28, 45]
		});
		mortesPolicial.addLayer(layer);
	} else if(feature.properties.tipo == "Roubo de Celular") {
		layer.options.icon = L.icon({
			iconUrl: "./img/roubocelular.png",
			iconSize: [28, 45]
		});
		roubosCelular.addLayer(layer);
	} else if(feature.properties.tipo == "Roubo de Veiculo") {
		layer.options.icon = L.icon({
			iconUrl: "./img/rouboveiculo.png",
			iconSize: [28, 45]
		});
		roubosVeiculo.addLayer(layer);
	}
}

var points = omnivore.csv("/mapa-crime-sp/data/massa.csv").on('ready', function () {
	points.eachLayer(eachLayer);
	overlayMaps["Furto de Celular"] = furtosCelular;
	overlayMaps["Furto de Veículo"] = furtosVeiculo;
	overlayMaps["Homicidio"] = homicidios;
	overlayMaps["Latrocínio"] = latrocinios;
	overlayMaps["Lesão Seguida de Morte"] = lesaoMorte;
	overlayMaps["Morte por Intervenção Policial"] = lesaoMorte;
	overlayMaps["Roubo de Celular"] = roubosCelular;
	overlayMaps["Roubo de Veiculo"] = roubosVeiculo;
	
	L.control.layers(null, overlayMaps).addTo(mymap);
});