const QUnit = require('qunit');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const WindArrow = require('../static/wind_direction.js');

QUnit.module('WindArrow', function(hooks) {
    hooks.beforeEach(function() {
        // Simulate a DOM environment for testing
        const dom = new JSDOM(`<!DOCTYPE html><div id="wind-direction"></div>`);
        global.document = dom.window.document;
    });

    QUnit.test('constructor', function(assert) {
        // Test that the constructor correctly adjusts degrees and calculates radians
        let windArrow = new WindArrow(90);
        assert.equal(windArrow.degrees, 0, 'Degrees are correctly adjusted');
        assert.equal(windArrow.radians, 0, 'Radians are correctly calculated');
    });

    QUnit.test('createCanvas', function(assert) {
        // Test that the createCanvas method correctly sets the canvas width and height
        let windArrow = new WindArrow(90);
        let canvas = windArrow.createCanvas(350);
        assert.equal(canvas.width, 350, 'Canvas width is correctly set');
        assert.equal(canvas.height, 350, 'Canvas height is correctly set');
    });

    QUnit.test('appendCanvasToContainer', function(assert) {
        // Test that the appendCanvasToContainer method correctly appends the canvas to the container
        let windArrow = new WindArrow(90);
        windArrow.createCanvas(350);
        windArrow.appendCanvasToContainer('wind-direction');
        let container = document.getElementById('wind-direction');
        assert.equal(container.firstChild, windArrow.canvas, 'Canvas is appended to container');
    });

    QUnit.test('calculateComponents', function(assert) {
        // Test that the calculateComponents method correctly calculates the x and y components
        let windArrow = new WindArrow(90);
        windArrow.calculateComponents();
        assert.equal(windArrow.x, 115, 'X component is correctly calculated');
        assert.equal(windArrow.y, 0, 'Y component is correctly calculated');
    });
});