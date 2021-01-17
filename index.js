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

class PlacesRequest extends XMLHttpRequest {
	constructor(inputString) {
		super();
		this.input = inputString;
		this.onreadystatechange = function() {
			if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
				let response = JSON.parse(this.responseText);
				if (response.places.length != 0) {
					for (var place of response.places) {
						/* Check the initial name is inside the place name */
						var regex = new RegExp(this.input, "i");
						if (regex.test(place[place.embedded_type].name)) {
							console.log("Ville: " + place[place.embedded_type].name + " " + place.id);
						}
					}
				}
				// Should change appearance of the cities table
			}
		};
	}
}

/* Useful API functions */
function loadRelevantPlaces(inputString) {
	let XHRPlaces = new PlacesRequest(inputString);
	XHRPlaces.open("GET", "https://api.sncf.com/v1/coverage/sncf/places?q=" + inputString);
	XHRPlaces.setRequestHeader("Authorization", apiKey);
	XHRPlaces.send();
}

/* Define components that will be watched during app run */
let cityA = document.getElementById("cityA");
let cityB = document.getElementById("cityB");

/* Listen to typing events */
cityA.addEventListener("input", function (){
	console.log("text: " + this.value);
	loadRelevantPlaces(this.value);
});

form.addEventListener('submit', onSubmit);
/* Define AJAX requests */
let XHRCityA = new XMLHttpRequest();
let XHRCityB = new XMLHttpRequest();


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
