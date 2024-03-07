// Assume value is retrieved from the database and passed to the template
var value = 1; // Example value
  
// Get the arrow and arrow value elements
const arrow = document.getElementById('arrowDR');

if (value === 1){
    value = 18;
}else if (value === 2){
    value = 39;    
} else if (value === 3){
    value = 59;    
}else if (value === 4){
    value = 80;
}

// Calculate the position of the arrow based on the value
const position = value + '%';

// Set the top position of the arrow and display the value
arrow.style.left = position;