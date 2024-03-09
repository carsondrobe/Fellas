// Assume value is retrieved from the database and passed to the template
const value = 92; // Example value
let position = value;

if (position > 100) {
    position = 100;
} else if (position < 0) {
    position = 0;
}
  
// Get the arrow and arrow value elements
const arrow = document.getElementById('arrow-ffmc');
const arrowValue = document.getElementById('arrowValue-ffmc');

// Calculate the top position of the arrow based on the value
let topPosition;

if (value < 80) {
    topPosition = 'calc(' + (100 - (position / 80) * 60) + '% - 15px)'; // Calculate the position relative to the top
} else {
    topPosition = 'calc(' + (100 - position) * 2 + '% - 15px)'; // Calculate the position position relative to the top

}

// Set the top position of the arrow and display the value
arrow.style.top = topPosition;
arrowValue.textContent = value;