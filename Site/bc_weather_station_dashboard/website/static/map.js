// Initialize map to open a focus around startup weather station
const map = L.map('map').setView([51, -121], 7);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

// Create customer marker icon
const markerIcon = L.icon({
    iconUrl: '../static/marker-icon.png',
    shadowUrl: "../static/marker-shadow.png",
    iconSize:    [25, 41],
    iconAnchor:  [12, 41],
    popupAnchor: [1, -34],
    shadowSize:  [41, 41]
});

// Create variable to hold current station's station code
var currentStationCode = 302;

// Fetch weather station information from Django backend
fetch('/weather_stations_information/')
    .then(response => response.json())
    .then(data => {
        // Create a marker for each weather station with a popup of information
        data.forEach(station => {
            var marker = L.marker([station.latitude, station.longitude], {icon: markerIcon})
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
            // Set HTML elements to show information of weather station with station code of currentStationCode on start with its popup activated
            if(station.code == currentStationCode) {
                document.getElementById('station-name-code').innerText = station.name + " - #" + station.code;
                updateData(currentStationCode);
                marker.fire('click');
            }
            // Add click event listener to update station name and code on click
            marker.on('click', function() {
                currentStationCode = station.code;
                document.getElementById('station-name-code').innerText = station.name + " - #" + station.code;
                updateData(currentStationCode);
            });
        });
    })
    .catch(error => console.error('Error fetching weather stations information:', error));

// Function to update the data on the right column
function updateData(stationCode) {
    // Get date from date picker
    var datePicker = document.getElementById('selected_date').innerHTML;
    if(datePicker === "Today") {
        // Format today's date to yyyy-mm-dd
        var year = new Date().getFullYear();
        var month = (new Date().getMonth() + 1).toString().padStart(2, '0');
        var day = new Date().getDate().toString().padStart(2, '0');
        datePicker = `${year}-${month}-${day}` + " 12:00:00";
    }
    var selectedDate = datePicker + " 12:00:00";
    // Fetch all of the data for the clicked station
    fetch(`/station_data/?datetime=${selectedDate}`)
        .then(response => response.json())
        .then(stationData => {
            // Set the current station's data dependant on the station code
            var currentStationData = stationData.find(measure => measure.STATION_CODE === stationCode);
            // Update HTML elements on right col
            updateDataHTML(currentStationData);
        })
    .catch(error => console.error('Error fetching station data:', error));
}

// Update HTML elements on right side
function updateDataHTML(currentStationData) {
    // Reset all values to "N/A"
    document.getElementById('temperature').innerHTML = "N/A";
    document.getElementById('relative-humidity').innerHTML = "N/A";
    document.getElementById('precipitation').innerHTML = "N/A";
    document.getElementById('snow-depth').innerHTML = "N/A";
    document.getElementById('snow-quality').innerHTML = "N/A";
    document.getElementById('wind-speed').innerHTML = "N/A";
    document.getElementById('wind-direction').innerHTML = "N/A";
    document.getElementById('wind-gust').innerHTML = "N/A";
    // Update the HTML elements with the station's temperature data
    if (currentStationData.HOURLY_TEMPERATURE) {
        document.getElementById('temperature').innerHTML = currentStationData.HOURLY_TEMPERATURE + " &deg;C";
    }

    // Update the HTML elements with the station's relative humidity data
    if (currentStationData.HOURLY_RELATIVE_HUMIDITY != null) {
        document.getElementById('relative-humidity').innerHTML = currentStationData.HOURLY_RELATIVE_HUMIDITY + " %";
    }

    // Update the HTML elements with the station's precipitation data
    if (currentStationData.HOURLY_PRECIPITATION) {
        document.getElementById('precipitation').innerHTML = currentStationData.HOURLY_PRECIPITATION + " mm";
    }

    // Update the HTML elements with the station's snow depth data
    if (currentStationData.SNOW_DEPTH) {
        document.getElementById('snow-depth').innerHTML = currentStationData.SNOW_DEPTH + " mm";
    }

    // Update the HTML elements with the station's snow quality data
    if (currentStationData.SNOW_DEPTH_QUALITY) {
        document.getElementById('snow-quality').innerHTML = currentStationData.SNOW_DEPTH_QUALITY + " mm";
    }

    // Update the HTML elements with the station's wind speed data
    if (currentStationData.HOURLY_WIND_SPEED) {
        document.getElementById('wind-speed').innerHTML = currentStationData.HOURLY_WIND_SPEED + " km/h";
    }

    // Update the HTML elements with the station's wind direction data
    if (currentStationData.HOURLY_WIND_DIRECTION) {
        document.getElementById('wind-direction').innerHTML = currentStationData.HOURLY_WIND_DIRECTION + "&deg;";
    }

    // Update the HTML elements with the station's wind gust data
    if (currentStationData.HOURLY_WIND_GUST) {
        document.getElementById('wind-gust').innerHTML = currentStationData.HOURLY_WIND_GUST;
    }
}

// Add event listener for change of selection of date picker, resets values of widgets to N/A before updating them so old values don't linger
document.getElementById('date_selector').addEventListener('change', function() {
    // Reset all elements here since an error caused by null value may not allow the request to make it to updateDataHTML
    document.getElementById('temperature').innerHTML = "N/A";
    document.getElementById('relative-humidity').innerHTML = "N/A";
    document.getElementById('precipitation').innerHTML = "N/A";
    document.getElementById('snow-depth').innerHTML = "N/A";
    document.getElementById('snow-quality').innerHTML = "N/A";
    document.getElementById('wind-speed').innerHTML = "N/A";
    document.getElementById('wind-direction').innerHTML = "N/A";
    document.getElementById('wind-gust').innerHTML = "N/A";
    // Update all data since date time is changing
    updateData(currentStationCode);
});

// Add event listener for clicks on map, resets values of widgets to N/A before updating them so old values don't linger
document.getElementById('map').addEventListener('click', function() {
    // Only need to update the HTML since date time is not changing
    updateDataHTML(currentStationCode);
});
