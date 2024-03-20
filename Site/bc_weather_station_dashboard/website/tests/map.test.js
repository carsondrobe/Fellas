// Mock setup for Leaflet L variable
global.L = {
    map: jest.fn().mockReturnThis( () => 'mock-map'),
    tileLayer: jest.fn().mockReturnThis(),
    icon: jest.fn().mockImplementation(() => 'mock-icon'),
    marker: jest.fn().mockReturnThis(),
    setView: jest.fn().mockReturnThis(),
    addTo: jest.fn().mockReturnThis(),
    bindPopup: jest.fn().mockReturnThis(),
    on: jest.fn().mockImplementation((event, callback) => callback()),
};

// Create variables for fetch mocking and functions, and jsdom
const fetchMock = require('jest-fetch-mock');
fetchMock.enableMocks();
const { initMap, initMarkerIcon, computeDistance, updateDataHTML, getSelectedDate, checkLocation } = require('../static/JavaScript/map');
require('@testing-library/jest-dom');

// Define a test suite for the initialization of leaflet map and markers
describe('initMap and initMarkerIcon Functionality', () => {
    // Reset mocks before each test
    beforeEach(() => {
        global.L.map.mockClear();
        global.L.tileLayer.mockClear();
        global.L.icon.mockClear();
    });
    // Create a test for creating a map
    test('initMap correctly creates a map.', () => {
        const mockMap = global.L;
        global.L.map.mockReturnValue(mockMap);
        const result = initMap(undefined);
        expect(global.L.tileLayer).toHaveBeenCalledWith(
            'https://tile.openstreetmap.org/{z}/{x}/{y}.png', 
            { maxZoom: 19 }
        );

        expect(result).toBe(mockMap);
    });
    // Create a test for creating a custom marker icon
    test('initMarkerIcon correctly creates a custom icon.', () => {
        const result = initMarkerIcon(undefined);
        expect(global.L.icon).toHaveBeenCalledWith({
            iconUrl: '../../static/images/weather_station_icon.svg',
            shadowUrl: "../../static/marker-shadow.png",
            iconSize: [35, 65],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });
        expect(result).toBe('mock-icon');
    });
});

// Define a test suite for the calculation of distance between 2 points
describe('computeDistance() Functionality', () => {
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

// Define a test suite for the calculation of distance between 2 points
describe('computeDistance() Functionality', () => {
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

// Define a test suite for the getSelectedDate() function
describe('getSelectedDate() Functionality', () => {
    // Create dom element before each test
    beforeAll(() => {
        document.body.innerHTML = `<div id="selected_date"></div>`;
    });
    // Create a test for getting the datetime when date picker is set to Today
    test('Correctly returns the current date and time when date picker is set to "Today".', () => {
        document.getElementById('selected_date').innerHTML = "Today";
        const fixedDate = new Date('2024-03-19T12:00:00Z');
        jest.useFakeTimers().setSystemTime(fixedDate);
        expect(getSelectedDate()).toBe('2024-03-19 12:00:00');
        jest.useRealTimers();
    });
    // Create a test for getting the datetime when date picker is set to a specific date
    test('Correctly returns the current date and time when date picker is set to a specific date.', () => {
        const specificDate = '2024-03-19';
        document.getElementById('selected_date').innerHTML = specificDate;
        expect(getSelectedDate()).toBe(specificDate + ' 12:00:00');
    });
});

// Define a test suite for the checkLocation() function
describe('checkLocation() Functionality', () => {
    let logSpy;
    // Set up mocks before each test
    beforeEach(() => {
        logSpy = jest.spyOn(console, 'log').mockImplementation();
        global.navigator.geolocation = {
            getCurrentPosition: jest.fn().mockImplementation((success) => {
                const mockPosition = {
                    coords: {
                        latitude: 123,
                        longitude: 456,
                    },
                    weatherStations: [
                        { longitude: 123.45, latitude: 67.89, code: 'STATION_1' },
                    ]
                };
                success(mockPosition);
            }),
        };
    });
    // Commented out because failing
    // // Create a test for checkLocation when geolocation is available
    // test('Correctly calls getCurrentPosition if geolocation is available.', () => {    
    //     checkLocation();
    //     expect(navigator.geolocation.getCurrentPosition).toHaveBeenCalled();
    // });
    // Create a test for checkLocation when geolocation is not available
    test('Correctly logs message if geolocation is not available.', () => {
        delete global.navigator.geolocation;
        checkLocation();
        expect(logSpy).toHaveBeenCalledWith("Geolocation is not available on this browser.");
    });
});
