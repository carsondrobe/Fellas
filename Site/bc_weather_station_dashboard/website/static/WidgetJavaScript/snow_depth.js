function drawSnowDepth(depth){
    if (depth === undefined || depth < 0){
        depth = 0;
    }
    depth = Math.round(depth/10);
    let container = document.getElementById('snow-depth');
    let snowImage = "/static/images/snow_container_empty.svg"
    let titleTag = `<h4>Snow Depth</h4>`;
    if (depth > 0 ){
        snowImage = "/static/images/snow_container.svg"
    }
    const imageTranslate = -3;
    let imageTag = `<img src="${snowImage}" style="
            transform: translateY(${imageTranslate}em); 
            min-width: 8em;
            z-index: -1;
        " width="90%"/>`;
    let depthTag = `<h3 style="
            color: #1a7fcc;
            z-index: 1;
            position: relative;
        " id="snow-value">${depth} cm</h3>`;
    if (depth === 0 ){
        depthTag = `<h4 style="
            color: #ffffff;
        " id="snow-value">No Snow</h4>`;
    }
    let snowDepthTag = `<div >${titleTag}${depthTag}${imageTag}</div>`;

    container.innerHTML = snowDepthTag;
    setSize();
}
function setSize(){
    let container = document.getElementById('snow-depth');
    let snowValue = document.getElementById('snow-value');
    if (window.innerWidth > 1000){
        container.style.maxHeight = `${13.5}em`;
        snowValue.style.transform = "translateY(2em)";
        console.log('big');
    } else {
        container.style.maxHeight = `${25}em`;
        snowValue.style.transform = "translateY(5em)";
        console.log('small');
    }
}
$(window).resize(function() {
  setSize();
});

drawSnowDepth(0);