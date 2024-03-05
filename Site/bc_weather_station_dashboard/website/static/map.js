// Initialize map to open a focus around startup weather station
const map = L.map('map').setView([51, -121], 7);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

const markerIcon = L.icon({
    iconUrl: '../static/marker-icon.png',
    shadowUrl: "../static/marker-shadow.png",

    iconSize:    [25, 41],
    iconAnchor:  [12, 41],
    popupAnchor: [1, -34],
    shadowSize:  [41, 41]
});

// Fetch data from Django backend
fetch('/weather_stations_data/')
    .then(response => response.json())
    .then(data => {
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
             // Set HTML elements to show information of weather station with id of 100 on start with its popup activated
            if(station['id'] == 100) {
                document.getElementById('station-name-code').innerText = station['name'] + " - #" + station['code'];
                marker.fire('click');
            }
            // Add click event listener to update station name and code on click
            marker.on('click', function() {
                document.getElementById('station-name-code').innerText = station.name + " - #" + station.id;
            });
        });
    })
    .catch(error => console.error('Error fetching weather station data:', error));