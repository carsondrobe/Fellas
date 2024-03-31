const { updateWindSpeed } = require('../../static/JavaScript/wind_speed.js');

QUnit.module("updateWindSpeed", hooks => {
    // Mock DOM setup
    const { JSDOM } = require("jsdom");
    const dom = new JSDOM(`<!DOCTYPE html><svg><circle></circle><text id="wind-gust"></text></svg>`);
    const { document } = dom.window;

    hooks.beforeEach(() => {
        global.document = document;
    });

    hooks.afterEach(() => {
        delete global.document;
    });

    const lightBlue = '#0dcaf0';
    const lightYellow = '#e0e064';
    const lightOrange = '#e68e47';
    const lightRed = '#e64c4c';

    const colorRanges = [
        { maxSpeed: 10, color: lightBlue },
        { maxSpeed: 15, color: lightYellow },
        { maxSpeed: 20, color: lightOrange },
        { maxSpeed: 30, color: lightRed }
    ];

    QUnit.test("Color update for varying wind speeds", assert => {
        // Mock circle element
        const circleElement = document.querySelector('circle');
        circleElement.getTotalLength = () => 100; // Mocking getTotalLength function

        // Test lightBlue color for windSpeed = 5
        updateWindSpeed(5, 10);
        assert.strictEqual(circleElement.style.stroke, lightBlue, "Wind speed of 5 sets circle color to lightBlue");

        // Test lightYellow color for windSpeed = 15
        updateWindSpeed(15, 20);
        assert.strictEqual(circleElement.style.stroke, lightYellow, "Wind speed of 15 sets circle color to lightYellow");

        // Test lightOrange color for windSpeed = 20
        updateWindSpeed(20, 25);
        assert.strictEqual(circleElement.style.stroke, lightOrange, "Wind speed of 20 sets circle color to lightOrange");

        // Test lightRed color for windSpeed = 35
        updateWindSpeed(35, 45);
        assert.strictEqual(circleElement.style.stroke, lightRed, "Wind speed of 35 sets circle color to lightRed");

        // Test lightRed color for windSpeed > maxWindSpeed
        updateWindSpeed(45, 50);
        assert.strictEqual(circleElement.style.stroke, lightRed, "Wind speed exceeding max sets circle color to lightRed");
    });
});
