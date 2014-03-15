function initializeSecond() {
	var mapOptions = {
		zoom: 10,
		center: new google.maps.LatLng({{latitude}}, {{longitude}})
	};

	var map = new google.maps.Map(document.getElementById('weather-canvas'), mapOptions);
	var weatherLayer = new google.maps.weather.WeatherLayer({
		temperatureUnits: google.maps.weather.TemperatureUnit.FAHRENHEIT
	});

	weatherLayer.setMap(map);

	var cloudLayer = new google.maps.weather.CloudLayer();
	cloudLayer.setMap(map);

	var marker = new google.maps.Marker({
		position: new google.maps.LatLng({{latitude}}, {{longitude}}),
		map: map,	
		title: "Your Location Again!"
	});
}
google.maps.event.addDomListener(window, 'load', initializeSecond);