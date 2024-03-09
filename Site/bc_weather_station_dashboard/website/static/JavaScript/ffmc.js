// Assume value_ffmc is retrieved from the database and passed to the template
const value_ffmc = 100; // Example value_ffmc
let position_ffmc = value_ffmc;

if (position_ffmc > 100) {
    position_ffmc = 100;
} else if (position_ffmc < 0) {
    position_ffmc = 0;
}
  
// Get the arrow and arrow value_ffmc elements
const arrow_ffmc = document.getElementById('arrow-ffmc');
const arrowvalue_ffmc = document.getElementById('arrowValue-ffmc');

// Calculate the top position_ffmc of the arrow based on the value_ffmc
let topposition_ffmc;

if (value_ffmc < 80) {
    topposition_ffmc = 'calc(' + (100 - (position_ffmc / 80) * 60) + '% - 15px)'; // Calculate the position_ffmc relative to the top
} else {
    topposition_ffmc = 'calc(' + (100 - position_ffmc) * 2 + '% - 15px)'; // Calculate the position_ffmc position_ffmc relative to the top

}

// Set the top position_ffmc of the arrow and display the value_ffmc
arrow_ffmc.style.top = topposition_ffmc;
arrowvalue_ffmc.textContent = value_ffmc;