// Assume value is retrieved from the database and passed to the template
const value = 62; // Example value
let position = value;

// Convert value to 80 if it is greater than 80 and convert value to 0 if it is less than 0
if (position > 80) {
    position = 80;
}
if (position < 0) {
    position = 0;
}
  
// Get the arrow and arrow value elements
const arrow = document.getElementById('arrow-dmc');
const arrowValue = document.getElementById('arrowValue-dmc');

// Calculate the top position of the arrow based on the value
const topPosition = 'calc(' + (100 - (position / 80) * 100) + '% - 15px)'; // Calculate the top position

// Set the top position of the arrow and display the value
arrow.style.top = topPosition;
arrowValue.textContent = value;
