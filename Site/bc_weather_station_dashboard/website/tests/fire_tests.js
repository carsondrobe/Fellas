// Import necessary modules and setup JSDOM environment
const fs = require('fs');
const path = require('path');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

const html = fs.readFileSync(path.resolve(__dirname, '../templates/fire.html'), 'utf8');
const { document } = (new JSDOM(html)).window;

global.document = document;

// FFMC tests

// Import the updateFFMC function
const { updateFFMC } = require('../static/dataLogic/ffmc.js');

// Define a test suite for the updateFFMC function
QUnit.module('updateFFMC', function() {
    // Test the updateFFMC function with a value of 50
    QUnit.test('value 50', function(assert) {
        updateFFMC(50);
        assert.equal(document.getElementById('arrow-ffmc').style.top, 'calc(62.5% - 5px)', 'Arrow top position is correct for value 50');
        assert.equal(document.getElementById('arrowValue-ffmc').textContent, '50', 'Arrow value is correct for value 50');
    });

    // Test the updateFFMC function with a value of 120
    QUnit.test('value 120', function(assert) {
        updateFFMC(120);
        assert.equal(document.getElementById('arrow-ffmc').style.top, 'calc(0% - 5px)', 'Arrow top position is correct for value 120');
        assert.equal(document.getElementById('arrowValue-ffmc').textContent, '120', 'Arrow value is correct for value 120');
    });

    // Test the updateFFMC function with a value of -10
    QUnit.test('value -10', function(assert) {
        updateFFMC(-10);
        assert.equal(document.getElementById('arrow-ffmc').style.top, 'calc(100% - 5px)', 'Arrow top position is correct for value -10');
        assert.equal(document.getElementById('arrowValue-ffmc').textContent, '0', 'Arrow value is correct for value -10');
    });
});
// End of FFMC tests

// DMC tests

// Import the updateDMC function
const { updateDMC } = require('../static/dataLogic/dmc.js');

// Define a test suite for the updateDMC function
QUnit.module('updateDMC', function() {
    // Test the updateDMC function with a value of 50
    QUnit.test('value 50', function(assert) {
        updateDMC(50);
        assert.equal(document.getElementById('arrow-dmc').style.top, 'calc(37.5% - 5px)', 'Arrow top position is correct for value 50');
        assert.equal(document.getElementById('arrowValue-dmc').textContent, '50', 'Arrow value is correct for value 50');
    });

    // Test the updateDMC function with a value of 120
    QUnit.test('value 100', function(assert) {
        updateDMC(100);
        assert.equal(document.getElementById('arrow-dmc').style.top, 'calc(0% - 5px)', 'Arrow top position is correct for value 100');
        assert.equal(document.getElementById('arrowValue-dmc').textContent, '100', 'Arrow value is correct for value 100');
    });

    // Test the updateDMC function with a value of -10
    QUnit.test('value -10', function(assert) {
        updateDMC(-10);
        assert.equal(document.getElementById('arrow-dmc').style.top, 'calc(100% - 5px)', 'Arrow top position is correct for value -10');
        assert.equal(document.getElementById('arrowValue-dmc').textContent, '0', 'Arrow value is correct for value -10');
    });
});
// End of DMC tests

// DC tests

// Import the updateDC function
const { updateDC } = require('../static/dataLogic/dc.js');

// Define a test suite for the updateDC function
QUnit.module('updateDC', function() {
    // Test the updateDC function with a value of 50
    QUnit.test('value 50', function(assert) {
        updateDC(50);
        assert.equal(document.getElementById('arrow-dc').style.top, 'calc(95% - 5px)', 'Arrow top position is correct for value 50');
        assert.equal(document.getElementById('arrowValue-dc').textContent, '50', 'Arrow value is correct for value 50');
    });

    // Test the updateDC function with a value of 120
    QUnit.test('value 1000', function(assert) {
        updateDC(1000);
        assert.equal(document.getElementById('arrow-dc').style.top, 'calc(0% - 5px)', 'Arrow top position is correct for value 1000');
        assert.equal(document.getElementById('arrowValue-dc').textContent, '999', 'Arrow value is correct for value 1000');
    });

    // Test the updateDC function with a value of -10
    QUnit.test('value -10', function(assert) {
        updateDC(-10);
        assert.equal(document.getElementById('arrow-dc').style.top, 'calc(100% - 5px)', 'Arrow top position is correct for value -10');
        assert.equal(document.getElementById('arrowValue-dc').textContent, '0', 'Arrow value is correct for value -10');
    });
});
// End of DC tests

// ISI tests

// Import the updateISI function
const { updateISI } = require('../static/dataLogic/isi.js');

// Define a test suite for the updateISI function
QUnit.module('updateISI', function() {
    // Test the updateISI function with a value of 50
    QUnit.test('value 20', function(assert) {
        updateISI(20);
        assert.equal(document.getElementById('arrow-isi').style.left, 'calc(80% - 14px)', 'Arrow top position is correct for value 20');
        assert.equal(document.getElementById('arrowValue-isi').textContent, '20', 'Arrow value is correct for value 20');
    });

    // Test the updateISI function with a value of 120
    QUnit.test('value 100', function(assert) {
        updateISI(100);
        assert.equal(document.getElementById('arrow-isi').style.left, 'calc(100% - 14px)', 'Arrow top position is correct for value 100');
        assert.equal(document.getElementById('arrowValue-isi').textContent, '100', 'Arrow value is correct for value 100');
    });

    // Test the updateISI function with a value of -10
    QUnit.test('value -10', function(assert) {
        updateISI(-10);
        assert.equal(document.getElementById('arrow-isi').style.left, 'calc(0% - 14px)', 'Arrow top position is correct for value -10');
        assert.equal(document.getElementById('arrowValue-isi').textContent, '0', 'Arrow value is correct for value -10');
    });
});
// End of ISI tests

// BUI tests

// Import the updateBUI function
const { updateBUI } = require('../static/dataLogic/bui.js');

// Define a test suite for the updateBUI function
QUnit.module('updateBUI', function() {
    // Test the updateBUI function with a value of 20
    QUnit.test('value 200', function(assert) {
        updateBUI(200);
        assert.equal(document.getElementById('arrow-bui').style.left, 'calc(80% - 14px)', 'Arrow left position is correct for value 200');
        assert.equal(document.getElementById('arrowValue-bui').textContent, '200', 'Arrow value is correct for value 200');
    });

    // Test the updateBUI function with a value of 100
    QUnit.test('value 500', function(assert) {
        updateBUI(500);
        assert.equal(document.getElementById('arrow-bui').style.left, 'calc(100% - 14px)', 'Arrow left position is correct for value 500');
        assert.equal(document.getElementById('arrowValue-bui').textContent, '500', 'Arrow value is correct for value 500');
    });

    // Test the updateBUI function with a value of -10
    QUnit.test('value -10', function(assert) {
        updateBUI(-10);
        assert.equal(document.getElementById('arrow-bui').style.left, 'calc(0% - 14px)', 'Arrow left position is correct for value -10');
        assert.equal(document.getElementById('arrowValue-bui').textContent, '0', 'Arrow value is correct for value -10');
    });
});

// End of BUI tests

// FWI tests

// Import the updateFWI function
const { updateFWI } = require('../static/dataLogic/fwi.js');

// Define a test suite for the updateFWI function
QUnit.module('updateFWI', function() {
    // Test the updateFWI function with a value of 20
    QUnit.test('value 20', function(assert) {
        updateFWI(20);
        assert.equal(document.getElementById('arrow-fwi').style.left, 'calc(40% - 14px)', 'Arrow left position is correct for value 20');
        assert.equal(document.getElementById('arrowValue-fwi').textContent, '20', 'Arrow value is correct for value 20');
    });

    // Test the updateFWI function with a value of 100
    QUnit.test('value 100', function(assert) {
        updateFWI(100);
        assert.equal(document.getElementById('arrow-fwi').style.left, 'calc(100% - 14px)', 'Arrow left position is correct for value 100');
        assert.equal(document.getElementById('arrowValue-fwi').textContent, '100', 'Arrow value is correct for value 100');
    });

    // Test the updateFWI function with a value of -10
    QUnit.test('value -10', function(assert) {
        updateFWI(-10);
        assert.equal(document.getElementById('arrow-fwi').style.left, 'calc(0% - 14px)', 'Arrow left position is correct for value -10');
        assert.equal(document.getElementById('arrowValue-fwi').textContent, '0', 'Arrow value is correct for value -10');
    });
});

// End of FWI tests

// dangerRating tests

// Import the function that updates the danger rating
const { updateDangerRating } = require('../static/dataLogic/danger_rating.js');

// Define a test suite for the updateDangerRating function
QUnit.module('updateDangerRating', function() {
    // Test the updateDangerRating function with a value of 1
    QUnit.test('value -1', function(assert) {
        updateDangerRating(-1);
        assert.equal(document.getElementById('arrow-danger-rating').style.left, '60px', 'Arrow left position is correct for value -1');
    });

    // Test the updateDangerRating function with a value of 1
    QUnit.test('value 1', function(assert) {
        updateDangerRating(1);
        assert.equal(document.getElementById('arrow-danger-rating').style.left, '60px', 'Arrow left position is correct for value 1');
    });

    // Test the updateDangerRating function with a value of 2
    QUnit.test('value 2', function(assert) {
        updateDangerRating(2);
        assert.equal(document.getElementById('arrow-danger-rating').style.left, '60px', 'Arrow left position is correct for value 2');
    });

    // Test the updateDangerRating function with a value of 3
    QUnit.test('value 3', function(assert) {
        updateDangerRating(3);
        assert.equal(document.getElementById('arrow-danger-rating').style.left, '164px', 'Arrow left position is correct for value 3');
    });

    // Test the updateDangerRating function with a value of 4
    QUnit.test('value 4', function(assert) {
        updateDangerRating(4);
        assert.equal(document.getElementById('arrow-danger-rating').style.left, '268px', 'Arrow left position is correct for value 4');
    });

    // Test the updateDangerRating function with a value of 5
    QUnit.test('value 5', function(assert) {
        updateDangerRating(5);
        assert.equal(document.getElementById('arrow-danger-rating').style.left, '372px', 'Arrow left position is correct for value 5');
    });

    // Test the updateDangerRating function with a value of 5
    QUnit.test('value 8', function(assert) {
        updateDangerRating(8);
        assert.equal(document.getElementById('arrow-danger-rating').style.left, '372px', 'Arrow left position is correct for value 8');
    });
});

// End of dangerRating tests