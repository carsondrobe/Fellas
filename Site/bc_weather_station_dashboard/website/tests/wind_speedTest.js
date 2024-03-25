const jsdom = require('jsdom');
const { JSDOM } = jsdom;

QUnit.module("updateWindSpeed", hooks => {
    // Mock environment setup
    let mockCircle;

    hooks.beforeEach(() => {
        // Mocking the DOM element that updateWindSpeed manipulates
        mockCircle = {
            style: {},
            getTotalLength: () => 100, // Assuming a circumference of 100 for simplicity
            setAttribute: function (attr, value) {
                this[attr] = value;
            }
        };

        // Mocking document.querySelector to return the mocked circle
        global.document = {
            querySelector: (selector) => {
                if (selector === 'circle:last-of-type') {
                    return mockCircle;
                }
            }
        };
    });

    hooks.afterEach(() => {
        // Cleanup
        delete global.document;
    });

    // Test cases
    QUnit.test("Color update for varying wind speeds", assert => {
        const { updateWindSpeed } = require('../static/JavaScript/wind_speed.js');

        updateWindSpeed(5); // Should set color to lightBlue
        assert.strictEqual(mockCircle.style.stroke, '#0dcaf0', "Wind speed of 5 sets circle color to lightBlue");

        updateWindSpeed(12); // Should set color to lightYellow
        assert.strictEqual(mockCircle.style.stroke, '#e0e064', "Wind speed of 12 sets circle color to lightYellow");

        updateWindSpeed(18); // Should set color to lightOrange
        assert.strictEqual(mockCircle.style.stroke, '#e68e47', "Wind speed of 18 sets circle color to lightOrange");

        updateWindSpeed(30); // Should set color to lightRed
        assert.strictEqual(mockCircle.style.stroke, '#e64c4c', "Wind speed of 30 sets circle color to lightRed");
    });

    QUnit.test("Stroke dashoffset updates correctly", assert => {
        const { updateWindSpeed } = require('../static/JavaScript/wind_speed.js');

        updateWindSpeed(10);
        // For a wind speed of 10, progressPercentage is (10/35)*100 = ~28.57%
        // Expected strokeDashoffset = 100 - 28.57 = ~71.43
        let actualDashoffset = parseFloat(mockCircle.style.strokeDashoffset).toFixed(2);
        assert.strictEqual(actualDashoffset, '71.43', "Wind speed of 10 sets correct strokeDashoffset");

        updateWindSpeed(35);
        // For max wind speed of 35, progressPercentage is 100%
        // Expected strokeDashoffset = 0
        actualDashoffset = mockCircle.style.strokeDashoffset.toString();
        assert.strictEqual(actualDashoffset, '0', "Max wind speed sets strokeDashoffset to 0");
    });
});
