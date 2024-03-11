class WindArrow {
    constructor(degrees) {
        // Adjust the degrees for compass-like behavior and convert to radians
        this.degrees = -(degrees - 90) % 360;
        this.radians = this.degrees * (Math.PI / 180);

        // Create a new canvas and set its dimensions
        this.canvas = document.createElement('canvas');
        this.canvas.width = this.canvas.height = 100;

        // 2D rendering context for the canvas
        this.ctx = this.canvas.getContext('2d');

        // Move the origin to the center of the canvas and invert the y-axis
        this.ctx.translate(this.canvas.width / 2, this.canvas.height / 2);
        this.ctx.scale(1, -1);
    }

    calculateComponents() {
        // Calculate the x and y components of the arrow
        this.x = 115 * Math.cos(this.radians);
        this.y = 115 * Math.sin(this.radians); 
    }

    drawMainArrow() {
        // Draw the main arrow in red
        this.ctx.beginPath();
        this.ctx.moveTo(0, 0);
        this.ctx.lineTo(this.x * 0.9, this.y * 0.9); // Shorten the line
        this.ctx.strokeStyle = 'red';
        this.ctx.lineWidth = 4;
        this.ctx.stroke();

        // Draw the arrowhead for the main arrow
        this.ctx.save();
        this.ctx.translate(this.x, this.y);
        this.ctx.rotate(this.radians);
        this.ctx.beginPath();
        this.ctx.moveTo(0, 0);
        this.ctx.lineTo(-15, -10);
        this.ctx.lineTo(-15, 10);
        this.ctx.closePath();
        this.ctx.fillStyle = 'red';
        this.ctx.fill();
        this.ctx.restore();
    }

    drawSecondaryArrow() {
        // Draw the secondary arrow in grey
        this.ctx.beginPath();
        this.ctx.moveTo(0, 0);
        this.ctx.lineTo(-this.x * 0.9, -this.y * 0.9); // Shorten the line
        this.ctx.strokeStyle = 'grey';
        this.ctx.lineWidth = 4;
        this.ctx.stroke();

        // Draw the arrowhead for the secondary arrow
        this.ctx.save();
        this.ctx.translate(-this.x, -this.y);
        this.ctx.rotate(this.radians + Math.PI); // Add 180 degrees to rotate in the opposite direction
        this.ctx.beginPath();
        this.ctx.moveTo(0, 0);
        this.ctx.lineTo(-15, -10);
        this.ctx.lineTo(-15, 10);
        this.ctx.closePath();
        this.ctx.fillStyle = 'grey';
        this.ctx.fill();
        this.ctx.restore();
    }

    drawCircle() {
        // Draw a circle
        this.ctx.beginPath();
        this.ctx.arc(0, 0, 160, 0, 2 * Math.PI);
        this.ctx.strokeStyle = 'black';
        this.ctx.lineWidth = 4; 
        this.ctx.stroke();
    }

    drawLabels() {
        // Draw labels for cardinal directions
        this.ctx.save();
        this.ctx.scale(1, -1);
        this.ctx.font = '30px Arial'; // font for the letters
        this.ctx.fillStyle = 'black';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText('S', 0, 140);  // position of the letter
        this.ctx.fillText('W', 140, 0);  
        this.ctx.fillStyle = 'red'; // Change fillStyle to red for 'N'
        this.ctx.fillText('N', 0, -140);  
        this.ctx.fillStyle = 'black'; // Change fillStyle back to black for 'E'
        this.ctx.fillText('E', -140, 0);
        this.ctx.restore();
    }
    drawAngleLabels() {
        // Draw smaller, grey labels for each 15 degrees
        // larger labels for each 30 degrees black
        this.ctx.save();
        this.ctx.scale(1, -1);
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        for (let angle = 0; angle < 360; angle += 15) {
            if (angle % 90 === 0) continue;
            let adjustedAngle = (90 - angle) % 360;
            if (adjustedAngle < 0) adjustedAngle += 360;
            let angleRad = adjustedAngle * (Math.PI / 180);
            let x = 1.40 * 100 * Math.cos(angleRad); 
            let y = 1.40 * 100 * Math.sin(angleRad); 
            let fontsize = angle % 30 === 0 ? '16px' : '12px';
            let color = angle % 30 === 0 ? 'black' : 'grey';
            this.ctx.font = fontsize + ' Arial';
            this.ctx.fillStyle = color;
            this.ctx.fillText(angle.toString(), x, -y);
        }
        this.ctx.restore();
    }

    draw() {
        console.log('draw method called');

        // Create a new canvas and set its dimensions
        this.canvas = document.createElement('canvas');
        this.canvas.width = this.canvas.height = 350; //this dictates the size of the canvas (still responsive)
        // Get the 2D rendering context for the canvas
        this.ctx = this.canvas.getContext('2d');

        // Move the origin to the center of the canvas and invert the y-axis
        this.ctx.translate(this.canvas.width / 2, this.canvas.height / 2);
        this.ctx.scale(1, -1);

        // Draw the wind arrow
        this.calculateComponents();
        this.drawMainArrow();
        this.drawSecondaryArrow();
        this.drawCircle();
        this.drawLabels();
        this.drawAngleLabels();

        // Append the canvas to the card with id 'wind-direction'
        let container = document.getElementById('wind-direction');
        this.canvas.style.maxWidth = '100%'; // for responsive canvas
        this.canvas.style.height = 'auto'; // for responsive canvas
        container.appendChild(this.canvas);
        console.log(this.ctx, container);
    }
}