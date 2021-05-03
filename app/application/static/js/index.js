
function checkCityResponse(cityResponse, cityInput) {
	if (cityResponse.places.length != 0) {
		citiesArray = [];
		for (var place of cityResponse.places) {
			/* Check the initial name is inside the place name */
			var regex = new RegExp(cityInput, "i");
			if (regex.test(place[place.embedded_type].name)) {
				if (place.embedded_type == "administrative_region") {
					citiesArray.push({"cityName": place[place.embedded_type].name, "id": place.id});
				}
				if (place.embedded_type == "stop_area") {
					citiesArray.push({"cityNameplace": place[place.embedded_type].name, "id": place[place.embedded_type].administrative_regions[0].id});
				}
			}
		}
		if (citiesArray.length == 0) {
			return undefined;
		}
		return citiesArray;
	} else {
		return undefined;
	}
}

function fillCityTable(cityInput, citiesArray) {
	let cityTable = cityInput.nextElementSibling;
	/* Flush table */
	cityTable.innerHTML = "";
	/* Fill table */
	for (var city of citiesArray) {
		var newRow = cityTable.insertRow();
		var newCell = newRow.insertCell();
		newCell.textContent = city.cityName;
		/* Fill the input cell when a city is clicked in the table */
		newCell.addEventListener('click', function() {
			cityInput.value = this.innerHTML;
			if (cityInput.name == 'departure') {
				document.getElementById('departure_id').value = city.id;
			}
			if (cityInput.name == 'arrival') {
				document.getElementById('arrival_id').value = city.id;
			}
			flushCityTable(cityInput);
		});
	}
	/* Make the cities array visible to user */
	cityTable.style.visibility = 'visible';
}

function flushCityTable(cityInput) {
	let parentDiv = cityInput.parentElement;
	let cityTable = cityInput.nextElementSibling;
	/* Flush table */
	cityTable.innerHTML = "";
	cityTable.visibility = 'hidden';
}

class PlacesRequest extends XMLHttpRequest {
	constructor(cityInput) {
		super();
		this.input = cityInput.value;
		/* If input is empty, flush the table */
		if (!this.input) {
			flushCityTable(cityInput);
		}
		this.onreadystatechange = function() {
			if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
				let response = JSON.parse(this.responseText);
				citiesArray = checkCityResponse(response, this.input);
				if (citiesArray) {
					fillCityTable(cityInput, citiesArray);
				} else {
					flushCityTable(cityInput);
				}
			}
		};
	}
}

/* Useful API functions */
function loadRelevantPlaces(cityInput) {
	let XHRPlaces = new PlacesRequest(cityInput);
	XHRPlaces.open("GET", "https://api.sncf.com/v1/coverage/sncf/places?q=" + cityInput.value);
	XHRPlaces.setRequestHeader("Authorization", window.appConfig.sncf_token);
	XHRPlaces.send();
}

/* Define components that will be watched during app run */
let departure = document.getElementById("departure");
let arrival = document.getElementById("arrival");

/* Listen to typing events */
departure.addEventListener("input", function() {
	loadRelevantPlaces(this);
});
arrival.addEventListener("input", function() {
	loadRelevantPlaces(this);
});
