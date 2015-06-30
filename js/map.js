// Eventify, Responsive HTML5 Event Template - Version 1.1 //

// Javascripts //
$(document).ready(function () {
	// Google Map //
	$('#map_canvas').gmap({
		'center': new google.maps.LatLng(43.696603, -79.692579), // Change this to your desired latitude and longitude
		'zoom': 13,
		'mapTypeControl': false,
		'navigationControl': false,
		'streetViewControl': false,
		'styles': [{
			stylers: [{
				gamma: 0.60
			}, {
				hue: "#31bda5"
			}, {
				invert_lightness: false
			}, {
				lightness: 2
			}, {
				saturation: -20
			}, {
				visibility: "on"
			}]
		}]
	});
	var image = {
		url: 'pics/marker.png', // Define the map marker file here
		// This marker is 51 pixels wide by 63 pixels tall.
		size: new google.maps.Size(76, 76),
		// The origin for this image is 0,0.
		origin: new google.maps.Point(0, 0),
		// The anchor for this image is the base of the flagpole at 26,63.
		anchor: new google.maps.Point(26, 63)
	};
	$('#map_canvas').gmap().bind('init', function () {
		$('#map_canvas').gmap('addMarker', {
			'id': 'marker-1',
			'position': '43.696603, -79.692579',
			'bounds': false,
			'icon': image
		}).click(function () {
			$('#map_canvas').gmap('openInfoWindow', {
				'content': '<h3><u>Redwood Studio</u></h3><p><strong>4 Alfred Kuehne Blvd.</strong><br>Brampton, ON<br> L6T 4N3</p>'
			}, this);
		});
	});
	
	// end		
});