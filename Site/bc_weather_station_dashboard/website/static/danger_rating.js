// Assume value is retrieved from the database and passed to the template
var value = 1; // Example value
  
// Get the arrow and arrow value elements
const arrow = document.getElementById('arrow-fire-rating');

if (value === 1 || value === 2){
    value = 64;
}else if (value === 3){
    value = 168;    
} else if (value === 4){
    value = 272;    
}else if (value === 5){
    value = 376;
}

// Calculate the position of the arrow based on the value
const position = value + 'px';

// Set the position of the arrow relative to the left
arrow.style.left = position;