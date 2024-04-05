function drawSnowDepth(depth){
    if (depth === undefined || depth < 0){
        depth = 0;
    }
    depth = Math.round(depth);
    let container = document.getElementById('snow-depth');
    let snowImage = "/static/images/snow_container_empty.svg"
    let titleTag = `<h4>Snow Depth</h4>`;
    if (depth > 0 ){
        snowImage = "/static/images/snow_container.svg"
    }
    const imageTranslate = -3;
    let imageTag = `<img src="${snowImage}" style="
            transform: translateY(${imageTranslate}em) translateZ(1em); 
            min-width: 8em;
            z-index: -1;
        " width="90%"/>`;
    const depthTranslate = 2;
    let depthTag = `<h3 style="
            color: #0b22be;
            transform: translateY(${depthTranslate}em) translateZ(2em);
            z-index: 1;
            position: relative;
        ">${depth} mm</h3>`;
    if (depth === 0 ){
        depthTag = `<h4 style="
            color: #ffffff;
            transform: translateY(${depthTranslate}em);
            z-index: 1;
        ">No Snow</h4>`;
    }
    let snowDepthTag = `<div >${titleTag}${depthTag}${imageTag}</div>`;

    container.innerHTML = snowDepthTag;
    setHeight();
}
function setHeight(){
    let container = document.getElementById('snow-depth');
    if (window.innerWidth > 1000){
        container.style.maxHeight = `${12}em`;
    } else {
        container.style.maxHeight = `${30}em`;
    }
    console.log("Height set to: " + container.style.maxHeight);
}
$(window).resize(function() {
  setHeight();
});

drawSnowDepth(0);