// Assume value is retrieved from the database and passed to the template
let value = 100; // Example value

if (value > 100) {
    value = 100;
} else if (value < 0) {
    value = 0;
}
  
// Get the arrow and arrow value elements
const arrow = document.getElementById('arrow');
const arrowValue = document.getElementById('arrowValue');

// Calculate the top position of the arrow based on the value
let topPosition;

if (value < 80) {
    topPosition = 'calc(' + (100 - (value / 80) * 60) + '% - 20px)'; // Calculate the top position
} else {
    topPosition = 'calc(' + (100 - value) * 2 + '% - 20px)'; // Calculate the top position

}

// Set the top position of the arrow and display the value
arrow.style.top = topPosition;
arrowValue.textContent = value;