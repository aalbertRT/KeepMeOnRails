const apiKey = "ad768e1e-e644-4994-a7e4-1af009618915"
var form = document.getElementById("mainForm");

function checkExistingRequest(request) {
	/*request is a js object*/
	return true;
}

function insertRequestInDatabase(request) {
	/*request is a js object*/
}

/* Create a backend job that will check regularly when tickets are being sold. */
function createRequestJob(request) {
	/*request is a js object*/
	insertRequestInDatabase(request);
}

function onSubmit(event) {
	event.preventDefault();
	let formInput = {
		firstName: document.getElementById("firstName").value,
		phoneNumber: document.getElementById("phoneNumber").value,
		cityA: document.getElementById("cityA").value,
		cityB: document.getElementById("cityB").value,
		date: document.getElementById("date").value
	}
	console.log(fromInput);
	/*
	let XHR = new XMLHttpRequest();
	XHR.onreadystatechange = function () {
		if (this.readyState == new XMLHttpRequest.DONE && this.status == 200) {
			let response = JSON.parse(this.responseText);
			console.log(response);
		}
	};
	XHR.open("GET", )
	XHR.send();
	*/
	/* Test the API request */
	/* Test the DB insertion */
	/* Tob be activated once db is set up
	if (!checkExistingRequest(formInput)) {
		insertRequestInDatabase(formInput);
		createRequestJob(formInput);
	}
	*/
}

/*
 * cityResponse is a response to API request
 */
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

/*
 *
 */
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
			document.getElementById("cityA").value = this.innerHTML;
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
	XHRPlaces.setRequestHeader("Authorization", apiKey);
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

/*
let XHR = new XMLHttpRequest();
XHR.onreadystatechange = function () {
	console.log(this.status);
	if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
		let response = JSON.parse(this.responseText);
		console.log(response);
	}
};
//let url = "https://api.sncf.com/v1/coverage/sncf/stop_areas/stop_area:OCE:SA:87391003/departures?datetime=20210114T212401";
let url = "https://api.sncf.com/v1/coverage"

XHR.open("GET", url);
XHR.setRequestHeader("Authorization", apiKey);
XHR.send();
*/