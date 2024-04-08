function updateDMC(value_dmc) {
    // Get the arrow and arrow value elements
    const arrow_dmc = document.getElementById('arrow-dmc');
    const arrowValue_dmc = document.getElementById('arrowValue-dmc');

    if(value_dmc === undefined) {
        arrow_dmc.style.top = 'calc(' + 100 + '% - 5px)';
        arrowValue_dmc.textContent = 'N/A';
        return; // Return early to prevent the rest of the function from running
    }

    value_dmc = Math.round(value_dmc);
    let position_dmc = value_dmc;

    // check if value_dmc is less than 0 and set it to 0
    if(value_dmc < 0) {
        value_dmc = 0;
    }

    // Convert value_dmc to 80 if it is greater than 80 and convert value_dmc to 0 if it is less than 0
    if (position_dmc > 80) {
        position_dmc = 80;
    }
    if (position_dmc < 0) {
        position_dmc = 0;
    }

    // Calculate the top position of the arrow based on the value
    const topPosition_dmc = 'calc(' + (100 - (position_dmc / 80) * 100) + '% - 5px)'; // Calculate the top position

    // Set the top position of the arrow and display the value
    arrow_dmc.style.top = topPosition_dmc;
    arrowValue_dmc.textContent = value_dmc;
}

module.exports = { updateDMC };