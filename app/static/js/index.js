var form = document.getElementById("mainForm");

function onSubmit(event) {
	event.preventDefault();
	let formInput = {
		firstName: document.getElementById("firstName").value,
		email: document.getElementById("email").value,
		phoneNumber: document.getElementById("phoneNumber").value,
		cityA: document.getElementById("cityA").value,
		cityB: document.getElementById("cityB").value,
		date: document.getElementById("date").value
	}
	console.log(formInput);
	//form.reset();

	var request = new XMLHttpRequest();
	request.onreadystatechange = function() {
		if (request.readyState == XMLHttpRequest.DONE && request.status == 200) {
			var response = request.responseText
			console.log(response);
		}
	}
	request.open("POST", "/ajax/");
	request.setRequestHeader("Content-type", "application/json");
	request.send(JSON.stringify(formInput));
}


function checkCityResponse(cityResponse, cityInput) {
	if (cityResponse.places.length != 0) {
		citiesArray = [];
		for (var place of cityResponse.places) {
			/* Check the initial name is inside the place name */
			var regex = new RegExp(cityInput, "i");
			if (regex.test(place[place.embedded_type].name)) {
				//console.log("Ville: " + place[place.embedded_type].name + " " + place.id);
				citiesArray.push({"cityName": place[place.embedded_type].name, "id": place.id});
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
	let parentDiv = cityInput.parentNode;
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
			flushCityTable(cityInput);
		});
	}
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
let cityA = document.getElementById("cityA");
let cityB = document.getElementById("cityB");

/* Listen to typing events */
cityA.addEventListener("input", function() {
	loadRelevantPlaces(this);
});
cityB.addEventListener("input", function() {
	loadRelevantPlaces(this);
});

form.addEventListener('submit', onSubmit);