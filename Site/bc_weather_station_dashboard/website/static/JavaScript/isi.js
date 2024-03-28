function updateISI(value_isi) {
    // Get the arrow and arrow value elements
    const arrow_isi = document.getElementById('arrow-isi');
    const arrowValue_isi = document.getElementById('arrowValue-isi');

    if(value_isi === undefined) {
        arrow_isi.style.left = 'calc(' + 0 + '% - 14px)';
        arrowValue_isi.textContent = 'N/A';
        return; // Return early to prevent the rest of the function from running
    }

    value_isi = Math.round(value_isi);
    let position_isi = value_isi;

    // check if value_ISI is less than 0 and set it to 0
    if(value_isi < 0) {
        value_isi = 0;
    }

    // Convert position_isi to 480 if it is greater than 480 and convert position_isi to 0 if it is less than 0
    if (position_isi > 25) {
        position_isi = 25;
    }
    if (position_isi < 0) {
        position_isi = 0;
    }
    
    // Calculate the left position of the arrow based on the position
    const leftPosition_isi = 'calc(' + ((position_isi) * 4) + '% - 14px)'; // Calculate the left position

    // Set the left position of the arrow and display the value
    arrow_isi.style.left = leftPosition_isi;
    arrowValue_isi.textContent = value_isi;
}

module.exports = { updateISI };