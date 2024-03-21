// Assume value_fwi is retrieved from the database and passed to the template
const value_fwi = 30; // Example value
let position_fwi = value_fwi;

// Convert value_fwi to 120 if it is greater than 120 and convert value_fwi to 0 if it is less than 0
if (position_fwi > 50) {
    position_fwi = 50;
}
if (position_fwi < 0) {
    position_fwi = 0;
}
  
// Get the arrow and arrow value elements
const arrow_fwi = document.getElementById('arrow-fwi');
const arrowValue_fwi = document.getElementById('arrowValue-fwi');

// Calculate the top position of the arrow based on the value
const leftPosition_fwi = 'calc(' + ((position_fwi) * 2) + '% - 14px)'; // Calculate the top position

// Set the top position of the arrow and display the value
arrow_fwi.style.left = leftPosition_fwi;
arrowValue_fwi.textContent = value_fwi;