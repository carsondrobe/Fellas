// Create variables
var currentStationCode;
var weatherStations;
var map;
var markerIcon;

// Initialize map
map = initMap(map);

// Create custom marker icon
markerIcon = initMarkerIcon(markerIcon);

// Fetch weather station information from Django backend and store them in weatherStations variable
fetchWeatherStationInfo().then(ws => {
    weatherStations = ws;
});

// Function to initialize map
function initMap(map) {
    map = L.map('map').setView([51, -121], 6);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);
    return map;
}

// Function to initialize marker icon
function initMarkerIcon(markerIcon) {
    markerIcon = L.icon({
        iconUrl: '../../static/images/weather_station_icon.svg',
        shadowUrl: "../../static/marker-shadow.png",
        iconSize: [35, 65],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });
    return markerIcon;
}

// Create function to fetch weather station information
function fetchWeatherStationInfo() {
    return fetch('/weather_stations_information/')
        // Check response
        .then(response => {
            // If response is ok
            if (response.ok) {
                return response.json();
                // If response is error
            } else {
                throw new Error("Error: Could not fetch weather stations.");
            }
        })
        .then(data => {
            // Call function to get user location
            checkLocation();
            // Create marker for each weather station
            data.forEach(station => {
                createMarker(station, 0);
            });
            // Return data
            return data;
        })
        .catch(error => {
            console.error('Error fetching weather stations information:', error);
            return undefined;
        });
}

// Function to update the data on the right column
function updateData(stationCode) {
    // Return date from date picker and fetch all of the data for the clicked station
    return fetch("/station_data/?datetime=" + getSelectedDate())
        .then(response => {
            // If station data is found
            if (response.ok) {
                return response.json();
                // If station data for this datetime is not found/error occurs
            } else {
                alert("There is no data found for this station on " + getSelectedDate() + ". Please select another date.");
                throw new Error("There is no station data for this date or this station is missing some of its' data. Error code " + response.status + ".");
            }
        })
        .then(stationData => {
            if (stationData !== undefined) {
                // Set current station data to station with stationCode
                var currentStationData = stationData.find(measure => measure.STATION_CODE === stationCode);
                updateDataHTML(currentStationData);
            }
        })
        .catch(error => {
            console.error(error);
        });
}

// Update HTML elements on right side
function updateDataHTML(currentStationData) {
    if (currentStationData.HOURLY_TEMPERATURE) {
        document.getElementById('temperature').innerHTML = currentStationData.HOURLY_TEMPERATURE;
    }
    // Update the HTML elements with the station's relative humidity data
    if (currentStationData.HOURLY_RELATIVE_HUMIDITY != null) {
        // Get the relative humidity
        var relativeHumidity = currentStationData.HOURLY_RELATIVE_HUMIDITY;
        // Get the progress bar element
        const progressBarElement = document.querySelector('#humidity-progress-bar');
        // Create a new SemiCircleProgressBar with the progress bar element
        const progressBar = new SemiCircleProgressBar(progressBarElement);
        // Set the value of the progress bar to the relative humidity
        progressBar.setValue(relativeHumidity);
    }
    // Update the HTML elements with the station's precipitation data
    if (currentStationData.HOURLY_PRECIPITATION !== undefined) {
        document.getElementById('precipitation').innerHTML = currentStationData.HOURLY_PRECIPITATION + " mm";
    }
    // Update the HTML elements with the station's snow depth data
    if (currentStationData.SNOW_DEPTH) {
        // document.getElementById('snow-depth').innerHTML = currentStationData.SNOW_DEPTH + " mm";
        drawSnowDepth(currentStationData.SNOW_DEPTH);
    }else{
        drawSnowDepth(0);
    }
    // Update the HTML elements with the station's wind speed data
    if (currentStationData.HOURLY_WIND_SPEED) {
        document.getElementById('wind-speed').textContent = currentStationData.HOURLY_WIND_SPEED + " km/h";
        updateWindSpeed(currentStationData.HOURLY_WIND_SPEED);
    }
    // Update the HTML elements with the station's wind direction data
    if (currentStationData.HOURLY_WIND_DIRECTION) {
        // Get the wind direction in degrees
        var windDirectionDegrees = currentStationData.HOURLY_WIND_DIRECTION;
        // Update the text display append to the wind direction widget
        document.getElementById('wind-direction').innerHTML = "<h5>Wind Direction " + windDirectionDegrees + "&deg;</h5>";
        // Create a new WindArrow with the updated wind direction
        var windArrow = new WindArrow(windDirectionDegrees);
        windArrow.draw();
    }
    // Update the HTML elements with the station's wind gust data
    // if (currentStationData.HOURLY_WIND_GUST) {
    //     document.getElementById('wind-gust').innerHTML = currentStationData.HOURLY_WIND_GUST;
    // }
}

// Function to get the selected date from the date picker
function getSelectedDate() {
    var datePicker = document.getElementById('selected_date').innerHTML;
    if (datePicker === "Today") {
        var year = new Date().getFullYear();
        var month = (new Date().getMonth() + 1).toString().padStart(2, '0');
        var day = new Date().getDate().toString().padStart(2, '0');
        datePicker = `${year}-${month}-${day}`;
    }
    return datePicker + " 12:00:00";
}

// Function to check if geolocation is available
function checkLocation() {
    // If geolocation is available
    if (navigator.geolocation) {
        // Get current location of user
        navigator.geolocation.getCurrentPosition(getClosestStation);
    } else {
        // geolocation is not available
        console.log("Geolocation is not available on this browser.");
    }
}

// Function to get user's location 
function getClosestStation(position) {
    // Get user's longitude and latitude and set max
    var userLongitude = position.coords.longitude;
    var userLatitude = position.coords.latitude;
    // Set variables for max, datalist, and closest station
    var max = Number.MAX_VALUE;
    let datalist = document.getElementById('search-suggestions');
    var closestStation;
    // Go through all of the weather stations
    weatherStations.forEach(station => {
        // Get stations longitude and latitude
        var stationLongitude = station.longitude;
        var stationLatitude = station.latitude;
        // Compute distance between two points
        var tempDistance = computeDistance(userLongitude, userLatitude, stationLongitude, stationLatitude);
        // If tempDistance is less than max, this station code is equal to closestStationCode
        if (tempDistance < max) {
            // Save this weather station as closest
            max = tempDistance;
            currentStationCode = station.code;
            closestStation = station;
        }
        // Create an option element and add it to the datalist
        let option = document.createElement('option');
        option.value = station.name;
        datalist.appendChild(option);
    });
    // Create and display this station's marker on map
    createMarker(closestStation, 1);
}

// Function to create a marker with an option to display it (if display is 1, marker pop up is enabled)
function createMarker(station, display) {
    var marker = L.marker([station.latitude, station.longitude], { icon: markerIcon })
        .addTo(map)
        .bindPopup(
            `<b>Station ID: ${station.id}</b><br>` +
            `<b>Station Code: ${station.code}</b><br>` +
            `<b>Station Name: ${station.name}</b><br>` +
            `<b>Station Acronym: ${station.acronym}</b><br>` +
            `<b>Latitude: ${station.latitude}</b><br>` +
            `<b>Longitude: ${station.longitude}</b><br>` +
            `<b>Elevation: ${station.elevation}m</b><br>` +
            `<b>Install Date: ${station.install_date}</b>`
        );
    // Add click event listener to update station name and code on click
    marker.on('click', function () {
        currentStationCode = station.code;
        document.getElementById('station-name-code').innerText = station.name + " - #" + station.code;
        updateData(currentStationCode);
    });
    // If display is 1, display
    if (display === 1) {
        // Display current station's data and open its popup
        marker.fire('click');
        // Add current station's name and code to the dashboard
        document.getElementById('station-name-code').innerText = station.name + " - #" + station.code;
    }
}

// Function to compute the distance between 2 points using longitude and latitude
function computeDistance(longitude1, latitude1, longitude2, latitude2) {
    // Set variables to compute distance using Haversine equation
    var radius = 6371;
    var distLongitude = (longitude2 - longitude1) * (Math.PI / 180);
    var distLatitude = (latitude2 - latitude1) * (Math.PI / 180);
    var a = Math.sin(distLatitude / 2) * Math.sin(distLatitude / 2) + Math.cos((latitude1) * (Math.PI / 180)) * Math.cos((latitude2) * (Math.PI / 180)) * Math.sin(distLongitude / 2) * Math.sin(distLongitude / 2);
    var b = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return radius * b;
}

// Create variable to store event listeners in
var eventListeners = document.addEventListener('DOMContentLoaded', function () {
    // Add event listener for change of selection of date picker, resets values of widgets to N/A before updating them so old values don't linger
    document.getElementById('date_selector').addEventListener('change', function () {
        // Reset all elements here since an error caused by null value may not allow the request to make it to updateDataHTML
        document.getElementById('temperature').innerHTML = "N/A";
        // document.getElementById('relative-humidity').innerHTML = "N/A";
        document.getElementById('precipitation').innerHTML = "N/A";
        document.getElementById('snow-depth').innerHTML = "N/A";
        document.getElementById('wind-speed').innerHTML = "N/A";
        document.getElementById('wind-direction').innerHTML = "N/A";
        // document.getElementById('wind-gust').innerHTML = "N/A";
        // Update all data since date time is changing
        updateData(currentStationCode);
    });

    // Add event listener for clicks on map, resets values of widgets to N/A before updating them so old values don't linger
    document.getElementById('map').addEventListener('click', function () {
        // Only need to update the HTML since date time is not changing
        updateDataHTML(currentStationCode);
    });

    // Function for displaying search bar station
    document.getElementById("search-btn").addEventListener("click", function () {
        // Set variable for input
        let input = document.getElementById('searchInput').value;
        // Go through all of the weather stations
        weatherStations.forEach(station => {
            // Display current station data if name matches
            if (station.name === input) {
                createMarker(station, 1);
            }
        });
    });
});

// Export functions for testing
module.exports = {
    initMap,
    initMarkerIcon,
    updateDataHTML,
    getSelectedDate,
    checkLocation,
    computeDistance
};