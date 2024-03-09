// Assume value_danger_rating is retrieved from the database and passed to the template
var value_danger_rating = 4; // Example value
  
// Get the arrow and arrow value elements
const arrow_danger_rating = document.getElementById('arrow-danger-rating');

if (value_danger_rating === 1 || value_danger_rating === 2){
    value_danger_rating = 60;
}else if (value_danger_rating === 3){
    value_danger_rating = 164;    
} else if (value_danger_rating === 4){
    value_danger_rating = 268;    
}else if (value_danger_rating === 5){
    value_danger_rating = 372;
}

// Calculate the position of the arrow based on the value_danger_rating
const position_danger_rating = value_danger_rating + 'px';

// Set the position of the arrow relative to the left
arrow_danger_rating.style.left = position_danger_rating;