// Mock setup for Leaflet L variable
global.L = {
    map: jest.fn().mockReturnThis(), 
    tileLayer: jest.fn().mockReturnThis(),
    icon: jest.fn().mockImplementation(() => 'mock-icon'),
    marker: jest.fn().mockReturnThis(),
    setView: jest.fn().mockReturnThis(),
    addTo: jest.fn().mockReturnThis(),
    bindPopup: jest.fn().mockReturnThis(),
    on: jest.fn().mockImplementation((event, callback) => callback()),
};

// Create variables for fetch mocking and functions
const fetchMock = require('jest-fetch-mock');
fetchMock.enableMocks();
const { computeDistance, updateDataHTML, createMarker } = require('../static/JavaScript/map');

require('@testing-library/jest-dom');

// Define a test suite for the calculation of distance between 2 points
describe('computeDistance() Functionality', () => {
    // Reset the fetch mock before each test
    beforeEach(() => {
        fetch.resetMocks();
    });
    // Create a test for computing the distance between two points that are not the same
    test('Correctly computes distance between two differing points.', () => {
        const distance = computeDistance(-121, 51, -122, 52);
        expect(distance).toBeCloseTo(130.977, 1);
    });
    // Create a test for computing the distance between two points that are the same
    test('Correctly computes distance between two of the same points.', () => {
        const distance = computeDistance(0, 0, 0, 0);
        expect(distance).toBeCloseTo(0, 0);
    });
});

// Define a test suite for the proper functioning of the updateDataHTML function
describe('updateDataHTML Functionality', () => {
    // Setup the document body to include elements that updateDataHTML tries to update and reset them
    beforeEach(() => {
        document.body.innerHTML = `
            <div id="temperature"></div>
            <div id="humidity-progress-bar"></div>
            <div id="precipitation"></div>
            <div id="snow-depth"></div>
            <div id="snow-quality"></div>
            <div id="wind-speed"></div>
            <div id="wind-direction"></div>
            <div id="wind-gust"></div>
        `;
    });
    // Temperature Widget
    test('Correctly updates temperature widget.', () => {
        const mockData = { HOURLY_TEMPERATURE: '25°C' };
        updateDataHTML(mockData);
        expect(document.getElementById('temperature')).toHaveTextContent('25°C');
    });
    test('Does not update the temp widget when data is missing.', () => {
        const mockData = {};
        updateDataHTML(mockData);
        expect(document.getElementById('temperature')).toHaveTextContent('');
    });
    // Precipitation Widget
    test('Correctly updates precipitation widget.', () => {
        const mockData = { HOURLY_PRECIPITATION: '10 mm' };
        updateDataHTML(mockData);
        expect(document.getElementById('precipitation')).toHaveTextContent('10 mm');
    });
    test('Does not update the precipitation widget when data is missing.', () => {
        const mockData = {};
        updateDataHTML(mockData);
        expect(document.getElementById('precipitation')).toHaveTextContent('');
    });
    // Snow Depth Widget
    test('Correctly updates snow depth widget.', () => {
        const mockData = { SNOW_DEPTH: '5 mm' };
        updateDataHTML(mockData);
        expect(document.getElementById('snow-depth')).toHaveTextContent('5 mm');
    });
    test('Does not update the snow depth widget when data is missing.', () => {
        const mockData = {};
        updateDataHTML(mockData);
        expect(document.getElementById('snow-depth')).toHaveTextContent('');
    });
    // Snow Quality Widget
    test('Correctly updates snow quality widget.', () => {
        const mockData = { SNOW_DEPTH_QUALITY: 'Good' };
        updateDataHTML(mockData);
        expect(document.getElementById('snow-quality')).toHaveTextContent('Good');
    });
    test('Does not update the snow quality widget when data is missing.', () => {
        const mockData = {};
        updateDataHTML(mockData);
        expect(document.getElementById('snow-quality')).toHaveTextContent('');
    });
    // Wind Speed Widget
    test('Correctly updates wind speed widget.', () => {
        const mockData = { HOURLY_WIND_SPEED: '15 km/h' };
        updateDataHTML(mockData);
        expect(document.getElementById('wind-speed')).toHaveTextContent('15 km/h');
    });
    test('Does not update the wind speed widget when data is missing.', () => {
        const mockData = {};
        updateDataHTML(mockData);
        expect(document.getElementById('wind-speed')).toHaveTextContent('');
    });
    // Wind Direction Widget
    test('Does not update the wind direction widget when data is missing.', () => {
        const mockData = {};
        updateDataHTML(mockData);
        expect(document.getElementById('wind-direction')).toHaveTextContent('');
    });
    // Wind Gust Widget
    test('Correctly updates wind gust widget.', () => {
        const mockData = { HOURLY_WIND_GUST: '20 km/h' };
        updateDataHTML(mockData);
        expect(document.getElementById('wind-gust')).toHaveTextContent('20 km/h');
    });
    test('Does not update the wind gust widget when data is missing.', () => {
        const mockData = {};
        updateDataHTML(mockData);
        expect(document.getElementById('wind-gust')).toHaveTextContent('');
    });
});

// Define a test suite for the proper functioning of the fetchWeatherStationInfo function
describe('Event Listeners Functionality', () => {
    // Before each test, set up the DOM environment and mock global functions and variables
    beforeEach(() => {
        document.body.innerHTML = `
            <select id="date_selector"></select>
            <div id="map"></div>
            <input id="searchInput" value="Station 1" />
            <button id="search-btn"></button>
            <div id="temperature">N/A</div>
            <div id="precipitation">N/A</div>
            <div id="snow-depth">N/A</div>
            <div id="snow-quality">N/A</div>
            <div id="wind-speed">N/A</div>
            <div id="wind-direction">N/A</div>
            <div id="wind-gust">N/A</div>
        `;
        jest.clearAllMocks();
        // Mock functions and variables
        global.updateData = jest.fn();
        global.updateDataHTML = jest.fn();
        global.createMarker = jest.fn().mockReturnThis();
        global.currentStationCode = 'Station 1 Code';
        global.weatherStations = [
            { name: "Station 1", id: 1 },
            { name: "Station 2", id: 2 },
        ];
        require('../static/JavaScript/map');
    });
    // Date Picker Change
    test('Date picker change resets widgets to N/A when data missing.', () => {
        const dateSelector = document.getElementById('date_selector');
        dateSelector.dispatchEvent(new Event('change'));
        expect(document.getElementById('temperature').innerHTML).toBe("N/A");
    });
    // Map Click
    test('Map click is registered.', () => {
        const map = document.getElementById('map');
        map.dispatchEvent(new Event('click'));
        expect(updateDataHTML).toHaveBeenCalled();
    });
    // Search Button Click
    test('Search button click displays data for the station matching search input.', () => {
        const searchBtn = document.getElementById('search-btn');
        searchBtn.dispatchEvent(new Event('click'));
        expect(createMarker).toHaveBeenCalledWith(expect.anything(), 1);
    });
});

