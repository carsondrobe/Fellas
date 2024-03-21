function rain() {
    var cloud = document.querySelector('.cloud');
    var e = document.createElement('div');
    var left = Math.floor(Math.random() * 105);
    var width = Math.random() * 3;
    var height = Math.random() * 13;
    var duration = Math.random() * 0.5;

    e.classList.add('raindrop');
    cloud.appendChild(e);
    e.style.top = '20px';
    e.style.left = 5 + left + 'px';;
    e.style.width = width + 'px';;
    e.style.height = height + 'px';;
    e.style.animationDuration = 1 + duration + 's'
    setTimeout(function() {
        cloud.removeChild(e)
    }, 2000)
}

// Lower number means more raindrops
setInterval(function() {
    rain()
}, 20);