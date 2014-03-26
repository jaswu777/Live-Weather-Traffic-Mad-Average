function initializeSecond() {
	var myLatLng = new google.maps.LatLng({{latitude}}, {{longitude}});

	var mapOptions = {
		zoom: 6,
		center: myLatLng
	};

	var map = new google.maps.Map(document.getElementById('weather-canvas'), mapOptions);
	var marker = new google.maps.Marker({
		position: myLatLng,
		map: map,	
		title: "Your Location Again!"
	});

	var cloudLayer = new google.maps.weather.CloudLayer();
	cloudLayer.setMap(map); 

	var weatherLayer = new google.maps.weather.WeatherLayer({
		temperatureUnits: google.maps.weather.TemperatureUnit.FAHRENHEIT
	}); 

	weatherLayer.setMap(map);
}
google.maps.event.addDomListener(window, 'load', initializeSecond);