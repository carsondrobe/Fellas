// Assume value is retrieved from the database and passed to the template
var value = 360; // Example value

// Convert value to 80 if it is greater than 80 and convert value to 0 if it is less than 0
if (value > 500) {
    value = 500;
}
if (value < 0) {
    value = 0;
}
  
// Get the arrow and arrow value elements
const arrow = document.getElementById('arrow-dc');
const arrowValue = document.getElementById('arrowValue-dc');

// Calculate the top position of the arrow based on the value
const topPosition = 'calc(' + (500 - value) / 5 + '% - 15px)'; // Calculate the top position

// Set the top position of the arrow and display the value
arrow.style.top = topPosition;
arrowValue.textContent = value;
