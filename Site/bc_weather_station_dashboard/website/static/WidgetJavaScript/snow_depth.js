function drawSnowDepth(depth){
    if (depth === undefined || depth < 0){
        depth = 0;
    }
    let container = document.getElementById('snow-depth');
    let loc = window.location.pathname;
    console.log("Current working directory: " + loc);
    let snowImage = "/static/images/snow_container_empty.svg"
    let titleTag = `<h4>Snow Depth</h4>`;
    if (depth > 0 ){
        snowImage = "/static/images/snow_container.svg"
    }
    const imageTranslate = -30;
    let imageTag = `<img src="${snowImage}" style="transform: translateY(${imageTranslate}px); min-width: 8em" width="90%"/>`;
    const depthTranslate = -5.2;
    let depthTag = `<h3 style="
            color: #0b22be;
            transform: translateY(${depthTranslate}em);
        ">${depth} mm</h3>`;
    if (depth === 0 ){
        depthTag = `<h4 style="
            color: #ffffff;
            transform: translateY(-6em);
        ">No Snow</h4>`;
    }
    let snowDepthTag = `<div >${titleTag}${imageTag}${depthTag}</div>`;
    container.innerHTML = snowDepthTag;
    let width = container.offsetWidth;
}

drawSnowDepth(0);