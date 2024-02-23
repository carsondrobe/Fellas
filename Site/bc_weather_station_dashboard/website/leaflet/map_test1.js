// Initialize map to open with a zoomed out view of BC
var map = L.map('map').setView([54.8, -125], 6);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// Create random weather stations for now
for(var i = 49; i <= 60; i += 2) {
    for(var j = 121; j <= 130; j += 2) {
        var marker = L.marker([i, -j]).addTo(map);
        var popup = marker.bindPopup('<b>Weather Station Name</b><br />Last Updated 6 minutes ago.');           
    }
}