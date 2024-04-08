// Import necessary modules and setup JSDOM environment
const fs = require('fs');
const path = require('path');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const QUnit = require('qunit');
const html = fs.readFileSync(path.resolve(__dirname, '../../templates/weather.html'), 'utf8');
const { document } = (new JSDOM(html)).window;
global.document = document;
const { getCurrentPrecipitationValue, clearIntervals } = require('../../static/widgetsJS/weather/precipitation');

// Define a test suite for the getCurrentPrecipitationValue function
QUnit.module('Precipitation Tests', function(hooks) {
    hooks.afterEach(() => {
        clearIntervals();
    });
    QUnit.test('getCurrentPrecipitationValue with number', function(assert) {
        document.getElementById('precipitation').innerText = '2.5';
        assert.equal(getCurrentPrecipitationValue(), 2.5, 'Should return 2.5 when precipitation text is "2.5"');
    });

    QUnit.test('getCurrentPrecipitationValue with non-number', function(assert) {
        document.getElementById('precipitation').innerText = 'N/A';
        assert.equal(getCurrentPrecipitationValue(), null, 'Should return null when precipitation text is "N/A"');
    });
});