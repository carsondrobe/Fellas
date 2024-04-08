function updateWindSpeed(windSpeed, windGust) {
    const blueColor = '#0dcaf0'; // Color for wind speed
    const darkBlueColor = '#447094'; // Darker shade of blue for wind gust
    const maxWindSpeed = 50;

    const windSpeedPercentage = (windSpeed / maxWindSpeed) * 100;
    const windGustPercentage = (windGust / maxWindSpeed) * 100;
    const circumference = 283; // Assuming the circumference of your circles

    // Update wind speed circle
    const windSpeedCircle = document.querySelector('.wind-speed-circle');
    windSpeedCircle.style.strokeDashoffset = circumference - (windSpeedPercentage / 100) * circumference;
    windSpeedCircle.style.stroke = blueColor;

    // Update wind gust circle
    const windGustCircle = document.querySelector('.wind-gust-circle');
    windGustCircle.style.strokeDashoffset = circumference - (windGustPercentage / 100) * circumference;
    windGustCircle.style.stroke = darkBlueColor;

    // Update wind speed text
    const windSpeedText = document.getElementById('wind-speed');
    windSpeedText.textContent = `${windSpeed} km/h`;
    windSpeedText.style.fill = blueColor; // For SVG text elements, use 'fill' instead of 'color'

    // Update wind gust text
    const windGustText = document.getElementById('wind-gust');
    windGustText.textContent = `${windGust} km/h`;
    windGustText.style.color = darkBlueColor;
}

module.exports.updateWindSpeed = updateWindSpeed;
