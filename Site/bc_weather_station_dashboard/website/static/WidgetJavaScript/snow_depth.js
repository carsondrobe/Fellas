function drawSnowDepth(depth){
    let container = document.getElementById('snow-depth');
    // console.log("CWD: " + process.cwd());
    let snowImage = "static/images/snow_container_empty.svg"
        titleTag = `<h4>Snow Depth</h4>`;
    if (depth > 0 ){
        snowImage = "static/images/snow_container.svg"
    }
    const imageTranslate = -30;
    if (depth > 0 ){
        snowImage = "static/images/snow_container.svg"
    }
    let imageTag = `<img src="${snowImage}" style="transform: translateY(${imageTranslate}px); min-width: 8em" width="90%"/>`;
    let depthTag = `<h3 style="
            color: #0b22be;
            transform: translateY(-5.2em);
        ">${depth} mm</h3>`;
    if (depth === 0 ){
        depthTag = `<h4 style="
            color: #ffffff;
            transform: translateY(-6em);
        ">No Snow</h4>`;
    }
    let snowDepthTag = `<div>${titleTag}${imageTag}${depthTag}</div>`;
    container.innerHTML = snowDepthTag;
    let width = container.offsetWidth;
    container.style.height = `${width*0.025 + 6}em`;
}

drawSnowDepth(10);