// Function to get current precipitation value
function getCurrentPrecipitationValue() {
    // Get precipitation amount
    var precipitationText = document.getElementById('precipitation').innerText;
    var match = precipitationText.match(/\d+(\.\d+)?/); 
    // If number, return number or else return null
    if (match) {
        return parseFloat(match[0]);
    } else {
        return null;
    }
}

// Function to change rain intensity
function adjustRainIntensity(precipitationValue) {
    // Calculate intensity
    var rainAmount;
    if(precipitationValue === 0) {
        rainAmount = 50000;
    } else if(precipitationValue <= 0.5) {
        rainAmount = 200;
    } else if(precipitationValue <= 1.0) {
        rainAmount = 150;
    } else if(precipitationValue <= 1.5) {
        rainAmount = 100;
    } else if(precipitationValue <= 2.0) {
        rainAmount = 60;
    } else if(precipitationValue <= 4.0) {
        rainAmount = 40;
    } else if(precipitationValue <= 6.0) {
        rainAmount = 20;
    } else {
        rainAmount = 5;
    }
    // Adjust raindrop intensity
    clearInterval(rainInterval);
    rainInterval = setInterval(rain, rainAmount)
}

// Function to create raindrops
function rain() {
    // Get cloud and create html div for raindrops
    var cloud = document.querySelector('.cloud');
    var e = document.createElement('div');
    var left = Math.floor(Math.random() * 105);
    var width = Math.random() * 3;
    var height = Math.random() * 13;
    var duration = Math.random() * 0.5;
    // Create raindrops
    e.classList.add('raindrop');
    cloud.appendChild(e);
    e.style.top = '20px';
    e.style.left = 5 + left + 'px';;
    e.style.width = width + 'px';;
    e.style.height = height + 'px';;
    e.style.animationDuration = 1 + duration + 's'
    setTimeout(function() {
        cloud.removeChild(e)
    }, 2000)
}

// Create rain interval variable
var rainInterval = setInterval(function() {
    rain()
}, 5000);

// Call rain intensity function every 3 milliseconds
setInterval(function() {
    adjustRainIntensity(getCurrentPrecipitationValue());
}, 300);

// Export for testing
module.exports = { getCurrentPrecipitationValue };