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

function updateWindSpeed(windSpeed, windGust) {
    let currentColor;
    for (const range of colorRanges) {
        if (windSpeed <= range.maxSpeed) {
            currentColor = range.color;
            break;
        }
    }

    const maxWindSpeed = 40;
    if (windSpeed >= 30) {
        currentColor = lightRed;
    }
    const progressPercentage = (windSpeed / maxWindSpeed) * 100;
    const progressCircle = document.querySelector('circle:last-of-type');
    const circumference = progressCircle.getTotalLength();
    progressCircle.style.strokeDashoffset = circumference - (progressPercentage / 100) * circumference;
    progressCircle.style.stroke = currentColor;

    const windGustText = document.getElementById('wind-gust');
    if (windGust > maxWindSpeed) {
        windGustText.style.color = lightRed;
    }
}

module.exports.updateWindSpeed = updateWindSpeed;

// Example usage:
// Call updateWindSpeed(windSpeed) where windSpeed is the value to be displayed.
