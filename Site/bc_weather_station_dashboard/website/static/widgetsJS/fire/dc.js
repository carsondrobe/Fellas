function updateDC(value_dc) {
    // Get the arrow and arrow value elements
    const arrow_dc = document.getElementById('arrow-dc');
    const arrowValue_dc = document.getElementById('arrowValue-dc');

    if(value_dc === undefined) {
        arrow_dc.style.top = 'calc(' + 100 + '% - 5px)';
        arrowValue_dc.textContent = 'N/A';
        return; // Return early to prevent the rest of the function from running
    }

    value_dc = Math.round(value_dc);

    // Convert position_dc to 500 if it is greater than 500 and convert position_dc to 0 if it is less than 0
    if (value_dc > 999) {
        value_dc = 999;
    }
    if (value_dc < 0) {
        value_dc = 0;
    }

    // Calculate the top position of the arrow based on the position_dc
    const topPosition_dc = 'calc(' + Math.round(100 - (value_dc / 1000) * 100) + '% - 5px)'; // Calculate the top position

    // Set the top position of the arrow and display the value_dc
    arrow_dc.style.top = topPosition_dc;
    arrowValue_dc.textContent = value_dc;
}

module.exports = { updateDC };