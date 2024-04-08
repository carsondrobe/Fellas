const { updateWindSpeed } = require('../../static/widgetsJS/weather/wind_speed.js');

QUnit.module("updateWindSpeed", hooks => {
    // Mock DOM setup
    const { JSDOM } = require("jsdom");
    const dom = new JSDOM(`<!DOCTYPE html>
                            <svg>
                                <circle class="wind-gust-circle"></circle>
                                <circle class="wind-speed-circle"></circle>
                                <text id="wind-speed"></text>
                                <text id="wind-gust"></text>
                            </svg>`);
    const { document } = dom.window;

    hooks.beforeEach(() => {
        global.document = document;
    });

    hooks.afterEach(() => {
        delete global.document;
    });

    const blueColor = '#0dcaf0';
    const darkBlueColor = '#447094';

    QUnit.test("Circle and Text Color Update for Wind Speed and Gust", assert => {
        // Mock circle elements
        const windSpeedCircle = document.querySelector('.wind-speed-circle');
        const windGustCircle = document.querySelector('.wind-gust-circle');
        windSpeedCircle.getTotalLength = windGustCircle.getTotalLength = () => 283; // Mocking getTotalLength function

        const windSpeedText = document.getElementById('wind-speed');
        const windGustText = document.getElementById('wind-gust');

        // Test blue color for windSpeed and dark blue for windGust
        updateWindSpeed(20, 30);
        assert.strictEqual(windSpeedCircle.style.stroke, blueColor, "Wind speed sets wind speed circle color to blue");
        assert.strictEqual(windGustCircle.style.stroke, darkBlueColor, "Wind gust sets wind gust circle color to dark blue");

        assert.strictEqual(windSpeedText.style.fill, blueColor, "Wind speed sets wind speed text color to blue");
        assert.strictEqual(windGustText.style.color, 'rgb(68, 112, 148)', "Wind gust sets wind gust text color to dark blue");
    });

    // Additional tests here as needed...
});
