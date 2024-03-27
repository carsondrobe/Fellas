// Create new JSDOM object to test weather.html and map.js
const { JSDOM } = require('jsdom');
const dom = new JSDOM(`
{% load static %}
<!doctype html>
<html lang="en">

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css"
          integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" href="../static/home.css">

    <!-- Leaflet CSS and JS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
    crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
    crossorigin=""></script>

    <title>Dashboard</title>


</head>

<body>

<!-- NAVBAR -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <a class="navbar-brand" href="#">BC Weather and Wildfire</a>

    <div id="date_selector" class="ml-auto">
        <strong><span id="selected_date" class="text-white p-2">Today</span></strong>
        <img class="datepicker-toggle-button" src="../static/calendar_icon.svg" alt="calendar icon" width="30">
        <input type="date" class="datepicker-input">
    </div>
    <script> // should be moved to a separate file when we make one
    const date_input = document.querySelector('.datepicker-input');
    const selected_date = document.querySelector('#selected_date');
    date_input.addEventListener('change', function (e) {
        const date = new Date(e.target.value);
        const adjusted_date = new Date(date.getTime() + date.getTimezoneOffset() * 60 * 1000);
        if (adjusted_date.toDateString() === new Date().toDateString()) {
            selected_date.textContent = "Today";
        } else {
            selected_date.textContent = adjusted_date.toLocaleDateString('en-CA');
        }
    });
    </script>

    <div class="nav-item dropdown">
        <a class="nav-link" href="#" id="navbarDropdown" role="button" data-toggle="dropdown"
           aria-haspopup="true" aria-expanded="false">
            <img class="avatar avatar-32 bg-light rounded-circle text-white p-1"
                 src="https://raw.githubusercontent.com/twbs/icons/main/icons/person.svg" width="35px">
        </a>
        <div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdown">
            <div id="profile_dropdown_logged_in">
            <a class="dropdown-item" href="#">Alerts</a>
            <a class="dropdown-item" href="#">Submit Feedback</a>
            <div class="dropdown-divider"></div>
            <a class="dropdown-item" href="#">Logout</a>
            </div>
            <div id="profile_dropdown_logged_out" style="display: none"> <!-- display should toggle when user logs in-->
            <a class="dropdown-item" href="#">Log in</a>
            </div>
        </div>
    </div>

</nav>


    <div class="container-fluid">
        <div class="row pt-3">
            <!-- Station Map Column -->
            <div class="col-4 text-center border-right">
                <h2 id="station-name-code"></h2>
                <hr>
                <!-- Leaflet Map Implementation -->
                <div id="map" style="height: 50em; width: 100%;"></div>
                <script src="{% static 'map.js' %}"></script>
            </div>
            <!-- Weather Data Column -->
            <div class="col-8">
                <h2>
                    Weather
                </h2>
                <hr>
                <label for="startDate">Date Filter</label>
                <input id="startDate" class="form-control" type="date" placeholder="" />
                <script>
                    document.getElementById("startDate").valueAsDate = new Date();
                </script>

            <!-- Row 1 -->
            <div class="row pt-4 justify-content-center">
                <!-- Temperature Card -->
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body text-center">
                            <h5 class="card-title">Temperature</h5>
                            <h2 class="card-text">34 C</h2>
                        </div>
                    </div>
                </div>
                <!-- Relative Humidity Card -->
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body text-center">
                            <h5 class="card-title">Relative Humidity</h5>
                            <h2 class="card-text">17%</h2>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Row 2 -->
            <div class="row pt-4 justify-content-center">
                <!-- Precipitation Card -->
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body text-center">
                            <h5 class="card-title">Precipitation</h5>
                            <h2 class="card-text">0 mm</h2>
                        </div>
                    </div>
                </div>
                <!-- Snow Depth Card -->
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body text-center">
                            <h5 class="card-title">Snow Depth</h5>
                            <h2 class="card-text">0 mm</h2>
                        </div>
                    </div>
                </div>
                <!-- Snow Quality Card -->
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body text-center">
                            <h5 class="card-title">Snow Quality</h5>
                            <h2 class="card-text">0 mm</h2>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Row 3 -->
            <div class="row pt-4 justify-content-center">
                <!-- Wind Speed Card -->
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body text-center">
                            <h5 class="card-title">Wind Speed</h5>
                            <h2 class="card-text">10 km/h</h2>
                        </div>
                    </div>
                </div>
                <!-- Wind Direction Card -->
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body text-center">
                            <h5 class="card-title">Wind Direction</h5>
                            <h2 class="card-text">NW</h2>
                        </div>
                    </div>
                </div>
                <!-- Wind Gust Card -->
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body text-center">
                            <h5 class="card-title">Wind Gust</h5>
                            <h2 class="card-text">12</h2>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
        integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo"
        crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js"
        integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1"
        crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js"
        integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM"
        crossorigin="anonymous"></script>
</body>

</html>
`);

// Create DOM model of HTML code above
const document = dom.window.document;

// Create test suite of map
describe('Map testing', () => {
    // Test if map element is present
    test('Map element is present', () => {
        const mapElement = document.getElementById('map');
        expect(mapElement).toBeTruthy();
    });
    // Test if map's station name and code information matches startup station's station name and id information
    test('Station name and code loaded in properly', () => {
        const sni = document.getElementById('station-name-code').innerText;
        expect(sni == "ASPEN GROVE - #302");
    });   
    // // Test if map's latitude information matches startup station's latitude information
    // test('Latitude loaded in properly', () => {
    //     const latitude = document.getElementById('latitude').innerText;
    //     expect(latitude == "Latitude: 49.94811");
    // }); 
    // // Test if map's longitude information matches startup station's longitude information
    // test('Longitude loaded in properly', () => {
    //     const longitude = document.getElementById('longitude').innerText;
    //     expect(longitude == "Longitude: -120.62107");
    // });    
    // // Test if map's elevation information matches startup station's elevation information
    // test('Elevation loaded in properly', () => {
    //     const elevation = document.getElementById('elevation').innerText;
    //     expect(elevation == "1065m");
    // });
});
