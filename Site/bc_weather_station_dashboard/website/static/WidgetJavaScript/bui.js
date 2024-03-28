function updateBUI(value_bui) {
    let position_bui = value_bui;

    // check if value_BUI is less than 0 and set it to 0
    if(value_bui < 0) {
        value_bui = 0;
    }

    // Convert value_bui to 250 if it is greater than 250 and convert value_bui to 0 if it is less than 0
    if (position_bui > 250) {
        position_bui = 250;
    }
    if (position_bui < 0) {
        position_bui = 0;
    }
    
    // Get the arrow and arrow value elements
    const arrow_bui = document.getElementById('arrow-bui');
    const arrowValue_bui = document.getElementById('arrowValue-bui');

    // Calculate the top position of the arrow based on the value
    const leftPosition_bui = 'calc(' + ((position_bui / 250) * 100) + '% - 14px)'; // Calculate the top position

    // Set the top position of the arrow and display the value
    arrow_bui.style.left = leftPosition_bui;
    arrowValue_bui.textContent = value_bui;
}

updateBUI(500);

module.exports = { updateBUI };