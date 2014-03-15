function initialize() {
	var myLatLng =  new google.maps.LatLng({{latitude}}, {{longitude}});
	var mapOptions = {
		zoom: 14,
		center: myLatLng
	}

	var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
	var trafficLayer = new google.maps.TrafficLayer();
	trafficLayer.setMap(map);
	var marker = new google.maps.Marker({
		position: myLatLng,
		map: map,
		title: "Your Location!"
	});
}
google.maps.event.addDomListener(window, 'load', initialize);