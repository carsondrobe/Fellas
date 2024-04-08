// Import necessary modules and setup JSDOM environment
const { JSDOM } = require('jsdom');
const { document } = (new JSDOM('')).window;
global.document = document;

// Import the SemiCircleProgressBar class
const SemiCircleProgressBar = require('../../static/widgetsJS/weather/humidity');

// Define a test suite for the SemiCircleProgressBar class
QUnit.module('SemiCircleProgressBar', function() {
    // Test the constructor of the SemiCircleProgressBar class
    QUnit.test('constructor', function(assert) {
        // Create a new instance of SemiCircleProgressBar and check if it's created and initialized correctly
        let container = document.createElement('div');
        let progressBar = new SemiCircleProgressBar(container, 50, '#0dcaf0', '#ddd', '#c0c0c0');
        assert.ok(progressBar, 'Instance created');
        assert.equal(progressBar.value, 50, 'Initial value set correctly');
    });

    // Test the setValue method of the SemiCircleProgressBar class
    QUnit.test('setValue', function(assert) {
        // Create a new instance of SemiCircleProgressBar, set a new value and check if it's updated correctly
        let container = document.createElement('div');
        let progressBar = new SemiCircleProgressBar(container, 0, '#0dcaf0', '#ddd', '#c0c0c0');
        progressBar.setValue(75);
        assert.equal(progressBar.value, 75, 'Value updated correctly');
    });

    // Test the setValue method with out of range values
    QUnit.test('setValue - out of range', function(assert) {
        // Create a new instance of SemiCircleProgressBar, set values out of range and check if they're capped correctly
        let container = document.createElement('div');
        let progressBar = new SemiCircleProgressBar(container, 0, '#0dcaf0', '#ddd', '#c0c0c0');
        progressBar.setValue(150);
        assert.equal(progressBar.value, 100, 'Value capped at 100');
        progressBar.setValue(-50);
        assert.equal(progressBar.value, 0, 'Value capped at 0');
    });

    // Test the update method of the SemiCircleProgressBar class
    QUnit.test('update', function(assert) {
        // Create a new instance of SemiCircleProgressBar, update its value and check if the visual representation is updated correctly
        let container = document.createElement('div');
        let progressBar = new SemiCircleProgressBar(container, 0, '#0dcaf0', '#ddd', '#c0c0c0');
        progressBar.setValue(50);
        progressBar.update();
        let offset = parseFloat(progressBar.arc.getAttribute('stroke-dashoffset'));
        assert.ok(offset > 0, 'Offset updated correctly');
    });
});