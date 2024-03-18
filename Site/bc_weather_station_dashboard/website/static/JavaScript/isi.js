// Assume value_isi is retrieved from the database and passed to the template
const value_isi = 10; // Example value
let position_isi = value_isi; // Inflate the position by 4

// Convert position_isi to 480 if it is greater than 480 and convert position_isi to 0 if it is less than 0
if (position_isi > 25) {
    position_isi = 25;
}
if (position_isi < 0) {
    position_isi = 0;
}
  
// Get the arrow and arrow value elements
const arrow_isi = document.getElementById('arrow-isi');
const arrowValue_isi = document.getElementById('arrowValue-isi');

// Calculate the left position of the arrow based on the position
const leftPosition_isi = 'calc(' + ((position_isi) * 4) + '% - 14px)'; // Calculate the left position

// Set the left position of the arrow and display the value
arrow_isi.style.left = leftPosition_isi;
arrowValue_isi.textContent = value_isi;