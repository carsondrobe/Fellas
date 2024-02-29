// Initialize map to open with a zoomed out view of BC
var map = L.map('map').setView([54.8, -125], 5);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

// Get data from BC_Wildfire_Active_Weather_Stations CSV
fetch('../data/BC_Wildfire_Active_Weather_Stations.csv').then(response => response.text()).then(data => {
    // Parse CSV data
    const rows = data.trim().split('\n');
    const titles = rows[0].split(',');
    const stations = rows.slice(1).map(row => {
        const data = row.split(',');
        const station = {};
        titles.forEach((title, index) => {
            station[title.trim()] = data[index].trim();
        });
        return station;
    });

    // Create markers for each weather station
    stations.forEach(station => {
        const marker = L.marker([parseFloat(station['Y']), parseFloat(station['X'])])
            .addTo(map)
            .bindPopup(
            '<b>Station ID: ' + station['WEATHER_STATIONS_ID'] + '</b><br>' +
            '<b>Station Code: ' + station['STATION_CODE'] + '</b><br>' +
            '<b>Station Name: ' + station['STATION_NAME'] + '</b><br>' +
            '<b>Station Acronym: ' + station['STATION_ACRONYM'] + '</b><br>' +
            '<b>Latitude: ' + station['LATITUDE'] + '</b><br>' +
            '<b>Longitude: ' + station['LONGITUDE'] + '</b><br>' +
            '<b>Elevation: ' + station['ELEVATION'] + '</b><br>' +
            '<b>Install Date: ' + station['INSTALL_DATE'] + '</b><br>'
            );
            
        // When marker is clicked on, change the variables in the left column to display information
        marker.on('click', function() {
            // Update HTML elements with marker's weather station information
            document.getElementById('station-name').innerText = station['STATION_NAME'] + " - #" + station['WEATHER_STATIONS_ID'];
            document.getElementById('latitude').innerText = 'Latitude: ' + station['LATITUDE'];
            document.getElementById('longitude').innerText = 'Longitude: ' + station['LONGITUDE'];
            document.getElementById('elevation').innerText = 'Elevation: ' + station['ELEVATION'] + "m";
        });
    });
});

