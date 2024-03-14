// Assume value_bui is retrieved from the database and passed to the template
const value_bui = 120; // Example value
let position_bui = value_bui;

// Convert value_bui to 500 if it is greater than 500 and convert value_bui to 0 if it is less than 0
if (position_bui > 120) {
    position_bui = 120;
}
if (position_bui < 0) {
    position_bui = 0;
}
  
// Get the arrow and arrow value elements
const arrow_bui = document.getElementById('arrow-bui');
const arrowValue_bui = document.getElementById('arrowValue-bui');

// Calculate the top position of the arrow based on the value
const leftPosition_bui = 'calc(' + ((position_bui / 120) * 100) + '% - 14px)'; // Calculate the top position

// Set the top position of the arrow and display the value
arrow_bui.style.left = leftPosition_bui;
arrowValue_bui.textContent = value_bui;