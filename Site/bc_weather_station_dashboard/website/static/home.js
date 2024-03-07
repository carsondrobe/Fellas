// For the card time "last updated at: " functionality
function showUpdatedTime(element) {
    element.textContent = "Last updated at: " + element.textContent;
}

function hideUpdatedTime(element) {
    element.textContent = element.textContent.replace("Last updated at: ", "");
}