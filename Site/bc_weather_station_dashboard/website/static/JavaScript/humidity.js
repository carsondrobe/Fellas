class SemiCircleProgressBar {
    constructor(element, initialValue = 0, strokeColor = '#4d4dff', trailColor = '#ddd', borderColor = '#c0c0c0') {
        element.innerHTML = ''; // Clear the element
        // Create SVG element
        this.svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        this.svg.setAttribute('viewBox', '0 0 100 50');
        this.svg.setAttribute('preserveAspectRatio', 'xMidYMid meet'); // scale to fit
        this.svg.style.shapeRendering = 'geometricPrecision'; // improve rendering make it less blurry

        // Create text element for percentage
        this.percentageText = document.createElementNS("http://www.w3.org/2000/svg", "text");
        this.percentageText.setAttribute('x', '50');
        this.percentageText.setAttribute('y', '38');
        this.percentageText.setAttribute('text-anchor', 'middle');
        this.percentageText.setAttribute('dominant-baseline', 'middle');
        this.percentageText.setAttribute('font-size', '15');
        this.percentageText.style.fill = '#fff'; 
        this.svg.appendChild(this.percentageText);

        // Create border path
        this.border = document.createElementNS("http://www.w3.org/2000/svg", "path");
        this.border.setAttribute('d', 'M 10 50 A 40 40 0 0 1 90 50');
        this.border.setAttribute('stroke', borderColor);
        this.border.setAttribute('fill', 'none');
        this.border.setAttribute('stroke-width', '12'); // border width
        this.border.setAttribute('stroke-linecap', 'round');
        this.svg.appendChild(this.border);

        // Create background path
        this.background = document.createElementNS("http://www.w3.org/2000/svg", "path");
        this.background.setAttribute('d', 'M 10 50 A 40 40 0 0 1 90 50');
        this.background.setAttribute('stroke', trailColor);
        this.background.setAttribute('fill', 'none');
        this.background.setAttribute('stroke-width', '10');
        this.background.setAttribute('stroke-linecap', 'round');
        this.svg.appendChild(this.background);

        // Create foreground path
        this.arc = document.createElementNS("http://www.w3.org/2000/svg", "path");
        this.arc.setAttribute('d', 'M 10 50 A 40 40 0 0 1 90 50');
        this.arc.setAttribute('stroke', strokeColor);
        this.arc.setAttribute('fill', 'none');
        this.arc.setAttribute('stroke-width', '10');
        this.arc.setAttribute('stroke-linecap', 'round');
        this.svg.appendChild(this.arc);

        // Create start border line
        this.startBorder = document.createElementNS("http://www.w3.org/2000/svg", "line");
        this.startBorder.setAttribute('x1', '15');
        this.startBorder.setAttribute('y1', '50');
        this.startBorder.setAttribute('x2', '5');
        this.startBorder.setAttribute('y2', '50');
        this.startBorder.setAttribute('stroke', borderColor);
        this.startBorder.setAttribute('stroke-width', '2');
        this.startBorder.setAttribute('shape-rendering', 'geometricPrecision');
        this.svg.appendChild(this.startBorder);

        // Create end border line
        this.endBorder = document.createElementNS("http://www.w3.org/2000/svg", "line");
        this.endBorder.setAttribute('x1', '85');
        this.endBorder.setAttribute('y1', '50');
        this.endBorder.setAttribute('x2', '95');
        this.endBorder.setAttribute('y2', '50');
        this.endBorder.setAttribute('stroke', borderColor);
        this.endBorder.setAttribute('stroke-width', '2');
        this.endBorder.setAttribute('shape-rendering', 'geometricPrecision');
        this.svg.appendChild(this.endBorder);

        // Append SVG to the provided element
        element.appendChild(this.svg);

        // Set initial value
        this.setValue(initialValue);
    }

    // Method to set value
    setValue(newValue) {
        // Ensure value is within 0-100 range
        if (newValue < 0) {
            newValue = 0;
        }

        if (newValue > 100) {
            newValue = 100;
        }
        this.value = newValue;
        this.percentageText.textContent = `${this.value}%`;
        this.update();
    }

    // Method to update the progress bar
    update() {
        // Calculate percentage that should be filled
        const percentage = this.value / 100;
        // Calculate circumference of the semicircle
        const circumference = Math.PI * 40; // 2 * pi * r, where r = 40
        // Calculate stroke-dashoffset used to create "empty" portion of the progress bar
        const offset = circumference * (1 - percentage); // offset for semicircle

        // Update stroke-dasharray and stroke-dashoffset
        this.arc.setAttribute('stroke-dasharray', `${circumference} ${circumference}`);
        this.arc.setAttribute('stroke-dashoffset', offset);
    }
}

// Usage:
document.addEventListener('DOMContentLoaded', (event) => {
    // Get element
    const elem = document.querySelector('#humidity-progress-bar');
    // Initialize the progress bar
    const progressBar = new SemiCircleProgressBar(elem, 0, '#4d4dff', '#ddd', '#c0c0c0');
    // Update the value
    progressBar.setValue(0); // sets the value of the bar
});