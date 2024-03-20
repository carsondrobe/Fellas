// Assume value_dc is retrieved from the database and passed to the template
let value_dc = 750; // Example value

// Convert position_dc to 500 if it is greater than 500 and convert position_dc to 0 if it is less than 0
if (value_dc > 999) {
    value_dc = 999;
}
if (value_dc < 0) {
    value_dc = 0;
}
  
// Get the arrow and arrow value elements
const arrow_dc = document.getElementById('arrow-dc');
const arrowValue_dc = document.getElementById('arrowValue-dc');

// Calculate the top position of the arrow based on the position_dc
const topPosition_dc = 'calc(' + (100 - (value_dc / 1000) * 100) + '% - 5px)'; // Calculate the top position

// Set the top position of the arrow and display the value_dc
arrow_dc.style.top = topPosition_dc;
arrowValue_dc.textContent = value_dc;