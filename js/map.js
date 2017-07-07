var mymap = L.map('mapid', {
	center: [-23.6824, -46.5957],
	zoom: 10
});

var overlayMaps = {};
var homicidios = L.markerClusterGroup();
var furtosCelular = L.markerClusterGroup();

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
	if(feature.properties.tipo == "Homicidio") {
		layer.options.icon = L.icon({
			iconUrl: "/mapa-crime-sp/img/homicidio.png",
			iconSize: [28, 45]
		});
		homicidios.addLayer(layer);
	} else if(feature.properties.tipo == "Furto de Celular") {
		layer.options.icon = L.icon({
			iconUrl: "/mapa-crime-sp/img/furto.png",
			iconSize: [28, 45]
		});
		furtosCelular.addLayer(layer);
	}
}

var points = omnivore.csv("/mapa-crime-sp/data/massa.csv").on('ready', function () {
	points.eachLayer(eachLayer);
	overlayMaps["Homicidio"] = homicidios;
	overlayMaps["Furto de Celular"] = furtosCelular;
	L.control.layers(null, overlayMaps).addTo(mymap);
});