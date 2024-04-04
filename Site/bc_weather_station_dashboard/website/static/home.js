// For the card time "last updated at: " functionality
function showUpdatedTime(element) {
    if(document.getElementById('selected_date').innerHTML == "Today") {
        element.textContent = "Updated " + element.textContent;
    } else {
        element.textContent = "Last updated at " + element.textContent;
    }
}

function hideUpdatedTime(element) {
    if(document.getElementById('selected_date').innerHTML == "Today") {
        element.textContent = element.textContent.replace("Updated ", "");

    } else {
        element.textContent = element.textContent.replace("Last updated at ", "");
    }
}